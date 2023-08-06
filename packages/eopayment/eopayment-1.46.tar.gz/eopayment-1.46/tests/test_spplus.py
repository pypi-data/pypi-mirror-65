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

import eopayment.spplus as spplus
from eopayment import ResponseError

import pytest


ntkey = b'58 6d fc 9c 34 91 9b 86 3f ' \
    b'fd 64 63 c9 13 4a 26 ba 29 74 1e c7 e9 80 79'

tests = [
    ('x=coin',
     'c04f8266d6ae3ce37551cce996c751be4a95d10a'),
    ('x=coin&y=toto',
     'ef008e02f8dbf5e70e83da416b0b3a345db203de'),
    ('x=wdwd%20%3Fdfgfdgd&z=343&hmac=04233b78bb5aff332d920d4e89394f505ec58a2a',
     '04233b78bb5aff332d920d4e89394f505ec58a2a')
]


def test_spplus():
    payment = spplus.Payment({'cle': ntkey, 'siret': '00000000000001-01'})

    for query, result in tests:
        assert spplus.sign_ntkey_query(ntkey, query).lower() == result

    with pytest.raises(ResponseError, match=r'missing reference, etat or refsfp'):
        payment.response('foo=bar')
