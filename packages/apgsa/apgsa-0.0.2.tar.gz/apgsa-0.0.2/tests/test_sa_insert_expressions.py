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
from .model import users

def test_insert_expression():

    # Test a sample of the SQL SA construct produces
    ins = users.insert()
    query = str(ins)
    assert query == 'INSERT INTO users (id, name, fullname) VALUES (:id, :name, :fullname)'

    # This can be limited by using the values() method, which establishes the VALUES clause of the INSERT explicitly
    ins = users.insert().values(name='jack', fullname='Jack Jones')
    assert str(ins) == 'INSERT INTO users (name, fullname) VALUES (:name, :fullname)'

    # Compiled form of the statement
    assert ins.compile().params == {'fullname': 'Jack Jones', 'name': 'jack'}
