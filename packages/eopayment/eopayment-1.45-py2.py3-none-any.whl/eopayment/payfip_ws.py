# eopayment - online payment library
# Copyright (C) 2011-2020 Entr'ouvert
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals

import copy
import datetime
from decimal import Decimal, ROUND_DOWN
import functools
import os
import random
import xml.etree.ElementTree as ET

from gettext import gettext as _

import six
from six.moves.urllib.parse import parse_qs

import zeep
import zeep.exceptions

from .systempayv2 import isonow
from .common import (PaymentCommon, PaymentResponse, URL, PAID, DENIED,
                     CANCELLED, ERROR, ResponseError, PaymentException)

WSDL_URL = 'https://www.tipi.budget.gouv.fr/tpa/services/mas_securite/contrat_paiement_securise/PaiementSecuriseService?wsdl'  # noqa: E501

SERVICE_URL = 'https://www.tipi.budget.gouv.fr/tpa/services/securite'  # noqa: E501

PAYMENT_URL = 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=%s'


def clear_namespace(element):
    def helper(element):
        if element.tag.startswith('{'):
            element.tag = element.tag[element.tag.index('}') + 1:]
        for subelement in element:
            helper(subelement)

    element = copy.deepcopy(element)
    helper(element)
    return element


class PayFiPError(PaymentException):
    def __init__(self, code, message, origin=None):
        self.code = code
        self.message = message
        self.origin = origin
        args = [code, message]
        if origin:
            args.append(origin)
        super(PayFiPError, self).__init__(*args)


class PayFiP(object):
    '''Encapsulate SOAP web-services of PayFiP'''

    def __init__(self, wsdl_url=None, service_url=None, zeep_client_kwargs=None):
        self.client = zeep.Client(wsdl_url or WSDL_URL, **(zeep_client_kwargs or {}))
        # distribued WSDL is wrong :/
        self.client.service._binding_options['address'] = service_url or SERVICE_URL

    def fault_to_exception(self, fault):
        if fault.message != 'fr.gouv.finances.cp.tpa.webservice.exceptions.FonctionnelleErreur' or fault.detail is None:
            return
        detail = clear_namespace(fault.detail)
        code = detail.find('FonctionnelleErreur/code')
        if code is None or not code.text:
            return PayFiPError('inconnu', ET.tostring(detail))
        descriptif = detail.find('FonctionnelleErreur/descriptif')
        libelle = detail.find('FonctionnelleErreur/libelle')
        return PayFiPError(
            code=code.text,
            message=(descriptif is not None and descriptif.text)
            or (libelle is not None and libelle.text)
            or '')

    def _perform(self, request_qname, operation, **kwargs):
        RequestType = self.client.get_type(request_qname)  # noqa: E501
        try:
            return getattr(self.client.service, operation)(RequestType(**kwargs))
        except zeep.exceptions.Fault as fault:
            raise self.fault_to_exception(fault) or PayFiPError('unknown', fault.message, fault)
        except zeep.exceptions.Error as zeep_error:
            raise PayFiPError('erreur-soap', str(zeep_error), zeep_error)

    def get_info_client(self, numcli):
        return self._perform(
            '{http://securite.service.tpa.cp.finances.gouv.fr/reponse}RecupererDetailClientRequest',
            'recupererDetailClient',
            numCli=numcli)

    def get_idop(self, numcli, saisie, exer, refdet, montant, mel, url_notification, url_redirect, objet=None):
        return self._perform(
            '{http://securite.service.tpa.cp.finances.gouv.fr/requete}CreerPaiementSecuriseRequest',
            'creerPaiementSecurise',
            numcli=numcli,
            saisie=saisie,
            exer=exer,
            montant=montant,
            refdet=refdet,
            mel=mel,
            urlnotif=url_notification,
            urlredirect=url_redirect,
            objet=objet)

    def get_info_paiement(self, idop):
        return self._perform(
            '{http://securite.service.tpa.cp.finances.gouv.fr/reponse}RecupererDetailPaiementSecuriseRequest',
            'recupererDetailPaiementSecurise',
            idOp=idop)


class Payment(PaymentCommon):
    '''Produce requests for and verify response from the TIPI online payment
    processor from the French Finance Ministry.

    '''

    description = {
        'caption': 'TIPI, Titres Payables par Internet',
        'parameters': [
            {
                'name': 'numcli',
                'caption': _(u'Client number'),
                'help_text': _(u'6 digits number provided by DGFIP'),
                'validation': lambda s: str.isdigit(s) and len(s) == 6,
                'required': True,
            },
            {
                'name': 'service_url',
                'default': SERVICE_URL,
                'caption': _(u'PayFIP WS service URL'),
                'help_text': _(u'do not modify if you do not know'),
                'validation': lambda x: x.startswith('http'),
            },
            {
                'name': 'wsdl_url',
                'default': WSDL_URL,
                'caption': _(u'PayFIP WS WSDL URL'),
                'help_text': _(u'do not modify if you do not know'),
                'validation': lambda x: x.startswith('http'),
            },
            {
                'name': 'saisie',
                'caption': _('Payment type'),
                'default': 'T',
                'choices': [
                    ('T', _('test')),
                    ('X', _('activation')),
                    ('W', _('production')),
                ],
            },
            {
                'name': 'normal_return_url',
                'caption': _('User return URL'),
                'required': True,
            },
            {
                'name': 'automatic_return_url',
                'caption': _('Asynchronous return URL'),
                'required': True,
            },
        ],
    }

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)
        wsdl_url = self.wsdl_url
        # use cached WSDL
        if wsdl_url == WSDL_URL:
            base_path = os.path.join(os.path.dirname(__file__), 'resource', 'PaiementSecuriseService.wsdl')
            wsdl_url = 'file://%s' % base_path
        self.payfip = PayFiP(wsdl_url=wsdl_url, service_url=self.service_url)

    def _generate_refdet(self):
        return '%s%010d' % (isonow(), random.randint(1, 1000000000))

    def request(self, amount, email, **kwargs):
        try:
            montant = Decimal(amount)
            # MONTANT must be sent as centimes
            montant = montant * Decimal('100')
            montant = montant.to_integral_value(ROUND_DOWN)
            if not (Decimal('0') < montant <= Decimal('10000000')):
                raise ValueError('MONTANT > 100000 euros or < 0')
            montant = str(montant)
        except ValueError:
            raise ValueError(
                'MONTANT invalid format, must be '
                'a decimal integer with less than 4 digits '
                'before and 2 digits after the decimal point '
                ', here it is %s' % repr(amount))

        numcli = self.numcli
        urlnotif = self.automatic_return_url
        urlredirect = self.normal_return_url
        exer = str(datetime.date.today().year)
        refdet = kwargs.get('refdet', self._generate_refdet())
        mel = email
        if hasattr(mel, 'decode'):
            mel = email.decode('ascii')

        try:
            if '@' not in mel:
                raise ValueError('no @ in MEL')
            if not (6 <= len(mel) <= 80):
                raise ValueError('len(MEL) is invalid, must be between 6 and 80')
        except Exception as e:
            raise ValueError('MEL is not a valid email, %r' % mel, e)

        # check saisie
        saisie = self.saisie
        if saisie not in ('T', 'X', 'W'):
            raise ValueError('SAISIE invalid format, %r, must be M, T, X or A' % saisie)

        idop = self.payfip.get_idop(numcli=numcli, saisie=saisie, exer=exer,
                                    refdet=refdet, montant=montant, mel=mel,
                                    url_notification=urlnotif,
                                    url_redirect=urlredirect)

        return str(idop), URL, PAYMENT_URL % idop

    def response(self, query_string, **kwargs):
        fields = parse_qs(query_string, True)
        idop = (fields.get('idop') or [None])[0]

        if not idop:
            raise ResponseError('missing idop parameter in query string')

        try:
            response = self.payfip.get_info_paiement(idop)
        except PayFiPError as e:
            raise ResponseError('invalid return from payfip', e)

        if response.resultrans == 'P':
            result = PAID
            bank_status = 'paid CB'
        elif response.resultrans == 'V':
            result = PAID
            bank_status = 'paid direct debit'
        elif response.resultrans == 'R':
            result = DENIED
            bank_status = 'refused CB'
        elif response.resultrans == 'Z':
            result = DENIED
            bank_status = 'refused direct debit'
        elif response.resultrans == 'A':
            result = CANCELLED
            bank_status = 'cancelled CB'
        else:
            result = ERROR
            bank_status = 'unknown result code: %r' % response.resultrans

        transaction_id = response.refdet
        transaction_id += ' ' + idop
        if response.numauto:
            transaction_id += ' ' + response.numauto

        return PaymentResponse(
            result=result,
            bank_status=bank_status,
            signed=True,
            bank_data={k: response[k] for k in response},
            order_id=idop,
            transaction_id=transaction_id,
            test=response.saisie == 'T')


if __name__ == '__main__':
    import click

    def show_payfip_error(func):
        @functools.wraps(func)
        def f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except PayFiPError as e:
                click.echo(click.style('PayFiP ERROR : %s "%s"' % (e.code, e.message), fg='red'))
        return f

    @click.group()
    @click.option('--wsdl-url', default=None)
    @click.option('--service-url', default=None)
    @click.pass_context
    def main(ctx, wsdl_url, service_url):
        import logging
        logging.basicConfig(level=logging.INFO)
        # hide warning from zeep
        logging.getLogger('zeep.wsdl.bindings.soap').level = logging.ERROR

        ctx.obj = PayFiP(wsdl_url=wsdl_url, service_url=service_url)

    def numcli(ctx, param, value):
        if not isinstance(value, six.string_types) or len(value) != 6 or not value.isdigit():
            raise click.BadParameter('numcli must a 6 digits number')
        return value

    @main.command()
    @click.argument('numcli', callback=numcli, type=str)
    @click.pass_obj
    @show_payfip_error
    def info_client(payfip, numcli):
        response = payfip.get_info_client(numcli)
        for key in response:
            print('%15s:' % key, response[key])

    @main.command()
    @click.argument('numcli', callback=numcli, type=str)
    @click.option('--saisie', type=click.Choice(['T', 'X', 'W']), required=True)
    @click.option('--exer', type=str, required=True)
    @click.option('--montant', type=int, required=True)
    @click.option('--refdet', type=str, required=True)
    @click.option('--mel', type=str, required=True)
    @click.option('--url-notification', type=str, required=True)
    @click.option('--url-redirect', type=str, required=True)
    @click.option('--objet', default=None, type=str)
    @click.pass_obj
    @show_payfip_error
    def get_idop(payfip, numcli, saisie, exer, montant, refdet, mel, objet, url_notification, url_redirect):
        idop = payfip.get_idop(numcli=numcli, saisie=saisie, exer=exer,
                               montant=montant, refdet=refdet, mel=mel,
                               objet=objet, url_notification=url_notification,
                               url_redirect=url_redirect)
        print('idOp:', idop)
        print(PAYMENT_URL % idop)

    @main.command()
    @click.argument('idop', type=str)
    @click.pass_obj
    @show_payfip_error
    def info_paiement(payfip, idop):
        print(payfip.get_info_paiement(idop))

    main()



