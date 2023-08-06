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

import asyncpg

from .dialect import _literalquery


class PGConnection(asyncpg.Connection):
    async def execute(self, query: str, *args, timeout: float = None) -> str:
        """
        Execute an SQLAlchemy command (or commands).

        """
        # postgresql dialect wedged
        literal_query = _literalquery(query)

        self._check_open()

        if not args:
            return await self._protocol.query(literal_query, timeout)

        _, status, _ = await self._execute(literal_query, args, 0, timeout, True)
        return status.decode()


async def connect(dsn=None, *,
                  host=None, port=None,
                  user=None, password=None, passfile=None,
                  database=None,
                  loop=None,
                  timeout=60,
                  statement_cache_size=100,
                  max_cached_statement_lifetime=300,
                  max_cacheable_statement_size=1024 * 15,
                  command_timeout=None,
                  ssl=None,
                  connection_class=PGConnection,
                  server_settings=None):
    return await asyncpg.connect(loop=loop, connection_class=connection_class,
        dsn=dsn, host=host, port=port, user=user, password=password, passfile=passfile,
        database=database, timeout=timeout, statement_cache_size=statement_cache_size,
        max_cached_statement_lifetime=max_cached_statement_lifetime,
        max_cacheable_statement_size=max_cacheable_statement_size,
        command_timeout=command_timeout, ssl=ssl, server_settings=server_settings)
