import pytest
from mock import AsyncMock, MagicMock


def test_general_arguments():
    from frankfurt import fields

    with pytest.raises(TypeError):
        fields.UUIDField(pk=True)


@pytest.mark.asyncio
async def test_fields_by_examples():

    conn = AsyncMock()
    conn.transaction = MagicMock()

    from frankfurt import Database, fields

    db = Database()

    class Example_1(db.Model):
        password = fields.BinaryField()

    await db.create_all_tables(conn=conn)

    conn.execute.assert_awaited_once_with(
        'CREATE TABLE IF NOT EXISTS "example_1" ("password" BYTEA)'
    )


def test_default_values():

    from frankfurt import Model, fields

    class Example(Model):
        text_1 = fields.CharField(max_length=200, default='text')
        text_2 = fields.CharField(max_length=200, default=None)
        text_3 = fields.CharField(max_length=200, default=lambda : "sentinel")

    example = Example()
    assert example['text_1'] == 'text'
    assert example['text_2'] is None
    assert example['text_3'] == 'sentinel'


def test_not_null_values():

    from frankfurt import Model, fields

    class Example(Model):
        text = fields.CharField(max_length=200, not_null=True)

    example = Example()

    with pytest.raises(KeyError):
        assert example['text'] is None


@pytest.mark.asyncio
async def test_unique_constraint():

    conn = AsyncMock()
    conn.transaction = MagicMock()

    from frankfurt import Database
    from frankfurt import fields

    db = Database()

    class Example(db.Model):
        token = fields.CharField(max_length=64, unique=True)

    await db.create_all_tables(conn=conn)

    conn.execute.assert_awaited_once_with(
        'CREATE TABLE IF NOT EXISTS "example" ("token" VARCHAR(64) UNIQUE)'
    )
