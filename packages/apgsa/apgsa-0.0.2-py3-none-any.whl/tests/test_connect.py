import pytest
import apgsa


@pytest.mark.asyncio
async def test_connect():
    conn = await apgsa.connect(user='test_user', password='test_pass',
                                database='test_db', host='127.0.0.1', connection_class=)
    # values = await conn.fetch('''SELECT * FROM mytable''')
    # assert b'expected result' == values
    await conn.close()


# import sqlalchemy as sa

# # @pytest.fixture(scope="module")
# def test_sa_engine():
#     """Create an engine of the sqlalchemy for each test case."""
#     engine = sa.create_engine('postgresql://test_user:test_pass@localhost/test_db', echo=True)  # lazy connecting
