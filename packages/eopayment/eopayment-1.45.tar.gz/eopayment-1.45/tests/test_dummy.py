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


import eopayment
import pytest


def test_dummy():
    options = {
        'direct_notification_url': 'http://example.com/direct_notification_url',
        'siret': '1234',
        'origin': 'Mairie de Perpette-les-oies'
    }
    p = eopayment.Payment('dummy', options)
    retour = (
        'http://example.com/retour?amount=10.0'
        '&direct_notification_url=http%3A%2F%2Fexample.com%2Fdirect_notification_url'
        '&email=toto%40example.com'
        '&transaction_id=6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
        '&return_url=http%3A%2F%2Fexample.com%2Fretour'
        '&nok=1'
    )
    r = p.response(retour.split('?', 1)[1])
    assert not r.signed
    assert r.transaction_id == '6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
    assert r.return_content is None
    retour = (
        'http://example.com/retour'
        '?amount=10.0'
        '&direct_notification_url=http%3A%2F%2Fexample.com%2Fdirect_notification_url'
        '&email=toto%40example.com'
        '&transaction_id=6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
        '&return_url=http%3A%2F%2Fexample.com%2Fretour'
        '&ok=1&signed=1'
    )
    r = p.response(retour.split('?', 1)[1])
    assert r.signed
    assert r.transaction_id == '6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
    assert r.return_content == 'signature ok'

    with pytest.raises(eopayment.ResponseError, match='missing transaction_id'):
        p.response('foo=bar')
