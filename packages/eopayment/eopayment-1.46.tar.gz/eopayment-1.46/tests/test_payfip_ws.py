# coding: utf-8
#
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

import json
import lxml.etree as ET

import httmock
import pytest

from zeep.plugins import HistoryPlugin

import eopayment
from eopayment.payfip_ws import PayFiP, PayFiPError


def xmlindent(content):
    if hasattr(content, 'encode') or hasattr(content, 'decode'):
        content = ET.fromstring(content)
    return ET.tostring(content, pretty_print=True).decode('utf-8', 'ignore')

NUMCLI = '090909'


# freeze time to fix EXER field to 2019
@pytest.fixture(autouse=True)
def freezer(freezer):
    freezer.move_to('2019-12-12')


class PayFiPHTTMock(object):
    def __init__(self, request):
        history_path = 'tests/data/payfip-%s.json' % request.function.__name__
        with open(history_path) as fd:
            self.history = json.load(fd)
        self.counter = 0

    @httmock.urlmatch()
    def mock(self, url, request):
        request_content, response_content = self.history[self.counter]
        self.counter += 1
        assert xmlindent(request.body) == request_content
        return response_content


@pytest.fixture
def payfip(request):
    history = HistoryPlugin()

    @httmock.urlmatch()
    def raise_on_request(url, request):
        # ensure we do not access network
        from requests.exceptions import RequestException
        raise RequestException('huhu')

    with httmock.HTTMock(raise_on_request):
        payfip = PayFiP(wsdl_url='file://eopayment/resource/PaiementSecuriseService.wsdl',
                        zeep_client_kwargs={'plugins': [history]})
    try:
        if 'update_data' not in request.keywords:
            with httmock.HTTMock(PayFiPHTTMock(request).mock):
                yield payfip
        else:
            yield payfip
    finally:
        # add @pytest.mark.update_data to test to update fixtures data
        if 'update_data' in request.keywords:
            history_path = 'tests/data/payfip-%s.json' % request.function.__name__
            d = [
                (xmlindent(exchange['sent']['envelope']),
                 xmlindent(exchange['received']['envelope']))
                for exchange in history._buffer
            ]
            content = json.dumps(d)
            with open(history_path, 'wb') as fd:
                fd.write(content)

# pytestmark = pytest.mark.update_data


def test_get_client_info(payfip):
    result = payfip.get_info_client(NUMCLI)
    assert result.numcli == NUMCLI
    assert result.libelleN2 == 'POUETPOUET'

NOTIF_URL = 'https://notif.payfip.example.com/'
REDIRECT_URL = 'https://redirect.payfip.example.com/'


def test_get_idop_ok(payfip):
    result = payfip.get_idop(
        numcli=NUMCLI,
        exer='2019',
        refdet='ABCDEFGH',
        montant='1000',
        mel='john.doe@example.com',
        objet='coucou',
        url_notification=NOTIF_URL,
        url_redirect=REDIRECT_URL,
        saisie='T')
    assert result == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'


def test_get_idop_refdet_error(payfip):
    with pytest.raises(PayFiPError, match='.*R3.*Le format.*REFDET.*conforme'):
        payfip.get_idop(
            numcli=NUMCLI,
            exer='2019',
            refdet='ABCD',
            montant='1000',
            mel='john.doe@example.com',
            objet='coucou',
            url_notification='https://notif.payfip.example.com/',
            url_redirect='https://redirect.payfip.example.com/',
            saisie='T')


def test_get_idop_adresse_mel_incorrect(payfip):
    with pytest.raises(PayFiPError, match='.*A2.*Adresse.*incorrecte'):
        payfip.get_idop(
            numcli=NUMCLI,
            exer='2019',
            refdet='ABCDEF',
            montant='9990000001',
            mel='john.doeexample.com',
            objet='coucou',
            url_notification='https://notif.payfip.example.com/',
            url_redirect='https://redirect.payfip.example.com/',
            saisie='T')


def test_get_info_paiement_ok(payfip):
    result = payfip.get_info_paiement('cc0cb210-1cd4-11ea-8cca-0213ad91a103')
    assert {k: result[k] for k in result} == {
        'dattrans': '12122019',
        'exer': '20',
        'heurtrans': '1311',
        'idOp': 'cc0cb210-1cd4-11ea-8cca-0213ad91a103',
        'mel': 'john.doe@example.com',
        'montant': '1000',
        'numauto': '112233445566-tip',
        'numcli': NUMCLI,
        'objet': 'coucou',
        'refdet': 'EFEFAEFG',
        'resultrans': 'V',
        'saisie': 'T'
    }


def test_get_info_paiement_P1(payfip):
    # idop par pas encore reçu par la plate-forme ou déjà nettoyé (la nuit)
    with pytest.raises(PayFiPError, match='.*P1.*IdOp incorrect.*'):
        payfip.get_info_paiement('cc0cb210-1cd4-11ea-8cca-0213ad91a103')


def test_get_info_paiement_P5(payfip):
    # idop reçu par la plate-forme mais transaction en cours
    with pytest.raises(PayFiPError, match='.*P5.*sultat de la transaction non connu.*'):
        payfip.get_info_paiement('cc0cb210-1cd4-11ea-8cca-0213ad91a103')


def test_payment_ok(request):
    payment = eopayment.Payment('payfip_ws', {
        'numcli': '090909',
        'automatic_return_url': NOTIF_URL,
        'normal_return_url': REDIRECT_URL,
    })

    with httmock.HTTMock(PayFiPHTTMock(request).mock):
        payment_id, kind, url = payment.request(
            amount='10.00',
            email='john.doe@example.com',
            # make test deterministic
            refdet='201912261758460053903194')

        assert payment_id == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'
        assert kind == eopayment.URL
        assert url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=cc0cb210-1cd4-11ea-8cca-0213ad91a103'

        response = payment.response('idop=%s' % payment_id)
        assert response.result == eopayment.PAID
        assert response.bank_status == 'paid CB'
        assert response.order_id == payment_id
        assert response.transaction_id == (
            '201912261758460053903194 cc0cb210-1cd4-11ea-8cca-0213ad91a103 112233445566-tip')


def test_payment_denied(request):
    payment = eopayment.Payment('payfip_ws', {
        'numcli': '090909',
        'automatic_return_url': NOTIF_URL,
        'normal_return_url': REDIRECT_URL,
    })

    with httmock.HTTMock(PayFiPHTTMock(request).mock):
        payment_id, kind, url = payment.request(
            amount='10.00',
            email='john.doe@example.com',
            # make test deterministic
            refdet='201912261758460053903194')

        assert payment_id == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'
        assert kind == eopayment.URL
        assert url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=cc0cb210-1cd4-11ea-8cca-0213ad91a103'

        response = payment.response('idop=%s' % payment_id)
        assert response.result == eopayment.DENIED
        assert response.bank_status == 'refused CB'
        assert response.order_id == payment_id
        assert response.transaction_id == '201912261758460053903194 cc0cb210-1cd4-11ea-8cca-0213ad91a103'


def test_payment_cancelled(request):
    payment = eopayment.Payment('payfip_ws', {
        'numcli': '090909',
        'automatic_return_url': NOTIF_URL,
        'normal_return_url': REDIRECT_URL,
    })

    with httmock.HTTMock(PayFiPHTTMock(request).mock):
        payment_id, kind, url = payment.request(
            amount='10.00',
            email='john.doe@example.com',
            # make test deterministic
            refdet='201912261758460053903194')

        assert payment_id == 'cc0cb210-1cd4-11ea-8cca-0213ad91a103'
        assert kind == eopayment.URL
        assert url == 'https://www.tipi.budget.gouv.fr/tpa/paiementws.web?idop=cc0cb210-1cd4-11ea-8cca-0213ad91a103'

        response = payment.response('idop=%s' % payment_id)
        assert response.result == eopayment.CANCELLED
        assert response.bank_status == 'cancelled CB'
        assert response.order_id == payment_id
        assert response.transaction_id == '201912261758460053903194 cc0cb210-1cd4-11ea-8cca-0213ad91a103'
