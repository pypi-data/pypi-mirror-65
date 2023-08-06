import pytest
from mock import AsyncMock


@pytest.mark.asyncio
async def test_create_table_no_columns():
    import frankfurt.sql

    conn = AsyncMock()

    ct = frankfurt.sql.CreateTable('test', {})
    await ct.execute(conn=conn)

    conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "test"'
    )


@pytest.mark.asyncio
async def test_create_table_with_many_columns():
    import frankfurt.sql

    conn = AsyncMock()

    columns = [
        frankfurt.sql.Column('col_0', f'dt_0'),
        frankfurt.sql.Column('col_1', f'dt_1')
    ]

    ct = frankfurt.sql.CreateTable('test', columns)
    await ct.execute(conn)
    conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "test" ("col_0" dt_0, "col_1" dt_1)'
    )


@pytest.mark.asyncio
async def test_simple_insert():
    import frankfurt.sql

    conn = AsyncMock()
    conn.fetchrow.return_value = {'a' : 1, 'b': 2}

    ins = frankfurt.sql.Insert('test', values={'a': 1}, returning=['a', 'b'])
    record = await ins.fetchrow(conn=conn)

    assert record['a'] == 1
    assert record['b'] == 2

    conn.fetchrow.assert_called_with(
        'INSERT INTO "test" ("a") VALUES ($1) RETURNING ("a", "b")', 1
    )
