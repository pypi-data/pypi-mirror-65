# MIT License

# Copyright (c) 2020 Kelvin Gao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest
import apgsa

from .model import users


@pytest.fixture
async def apgsa_conn():
    """
    Create an apgsa connection for each test case.

    """
    conn = await apgsa.connect(user='test_user', password='test_pass',
                                database='test_db', host='127.0.0.1')

    yield conn
    await conn.close()


@pytest.fixture
async def conn(apgsa_conn):
    yield apgsa_conn

    # teardown table users
    await apgsa_conn.execute(users.delete())


@pytest.mark.asyncio
async def test_executing(conn):
    ins = users.insert().values(name='jack', fullname='Jack Jones')

    # Test a sample of the SQL this construct produces
    status = await conn.execute(ins)
    assert status == 'INSERT 0 1'
