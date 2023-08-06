import pytest
from mock import AsyncMock, MagicMock, call


def test_simple_model():

    from frankfurt.models import Model
    from frankfurt import fields

    class Example(Model):
        text = fields.CharField(max_length=200)

    example = Example(text='test')
    assert example['text'] == 'test'

    with pytest.raises(KeyError):
        example['text_3']


def test_exception_incorrect_argument():
    from frankfurt.models import Model, HasNotFieldTypeError
    from frankfurt import fields

    class Example(Model):
        text = fields.CharField(max_length=200)

    with pytest.raises(HasNotFieldTypeError):
        Example(anoter='test')


def test_abstract_model():

    from frankfurt.models import Model

    class Example(Model):

        class Meta:
            abstract = True

    assert Example._meta.abstract


def test_inherit_fields():
    from frankfurt import Database
    from frankfurt import fields

    db = Database()

    class Writer(db.Model):
        pk = fields.UUIDField(primary_key=True)
        full_name = fields.CharField(max_length=400)

        class Meta:
            table_name = 'writers'

    class BaseModel(db.Model):
        pk = fields.UUIDField(primary_key=True)
        creation_date = fields.DateTimeField(auto_now_add=True)
        writer = fields.ForeignKeyField(to='writers')

        class Meta:
            abstract = True

    class Book(BaseModel):
        title = fields.CharField(max_length=200)


    # Check that book has the right fields.
    assert 'pk' in Book._meta.fields
    assert 'creation_date' in Book._meta.fields
    assert 'writer' in Book._meta.fields

    # Check that the fields are new instances.
    assert BaseModel._meta.fields['pk'] != Book._meta.fields['pk']
    assert BaseModel._meta.fields['pk'].model is BaseModel
    assert Book._meta.fields['pk'].model is Book


@pytest.mark.asyncio
async def test_create_table_from_model():
    from frankfurt.models import Model
    from frankfurt import fields

    conn = AsyncMock()

    class Writer(Model):
        pk = fields.UUIDField(primary_key=True)
        full_name = fields.CharField(max_length=400)

        class Meta:
            table_name = 'writers'

    class Book(Model):
        title = fields.CharField(max_length=200)
        date = fields.DateTimeField()
        author = fields.ForeignKeyField(to='writers')

        class Meta:
            table_name = 'books'

    await Book._meta.db.create_table(Book, conn=conn)

    # Assert the connection.
    conn.execute.assert_called_once_with(
        f'CREATE TABLE IF NOT EXISTS books (title VARCHAR(200), '
        'date TIMESTAMPTZ, author UUID REFERENCES writers (pk))'
    )


@pytest.mark.asyncio
async def test_create_all_tables_1():

    conn = AsyncMock()
    conn.transaction = MagicMock()

    from frankfurt.models import Database
    from frankfurt import fields

    db = Database()

    class Writer(db.Model):
        pk = fields.UUIDField(primary_key=True)
        full_name = fields.CharField(max_length=400)

        class Meta:
            table_name = 'writers'

    class Book(db.Model):
        title = fields.CharField(max_length=200)
        date = fields.DateTimeField()
        author = fields.ForeignKeyField(to='writers')

        class Meta:
            table_name = 'books'

    await db.create_all_tables(conn=conn)

    # Assert the connection.
    assert conn.execute.mock_calls == [
        call('CREATE TABLE IF NOT EXISTS writers '
             '(pk UUID PRIMARY KEY, full_name VARCHAR(400))'),
        call(f'CREATE TABLE IF NOT EXISTS books (title VARCHAR(200), '
             'date TIMESTAMPTZ, author UUID REFERENCES writers (pk))'),
    ]
