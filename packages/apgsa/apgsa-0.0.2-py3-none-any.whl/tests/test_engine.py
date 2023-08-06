import pytest
import asyncpg


# @pytest.mark.asyncio
# async def test_connect():
#     conn = await asyncpg.connect(user='test_user', password='test_pass',
#                                  database='test_db', host='127.0.0.1')
#     # values = await conn.fetch('''SELECT * FROM mytable''')
#     # assert b'expected result' == values
#     await conn.close()

from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
