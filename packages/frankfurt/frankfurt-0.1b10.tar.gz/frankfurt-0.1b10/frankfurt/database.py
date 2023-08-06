from typing import Tuple, Type, Dict, Any, List

import asyncpg

from .models import BaseModel
from .fields import ForeignKeyField, BaseField, Action

from . import sql


class Meta:
    abstract : bool = False
    name: str
    table_name : str
    fields : Dict[str, BaseField] = {}
    db: Any

    def __init__(self, name : str):
        self.name = name
        self.table_name = name.lower()
        self.fields = {}

    @property
    def depends(self):
        # Return a list of methods that should be created first.

        deps = []

        for field in self.fields.values():
            if isinstance(field, ForeignKeyField):
                deps.append(field.to_field.model)

        return deps

    def extend_from_model(self, Meta):

        # Set the db.
        if hasattr(Meta, 'db'):
            self.db = Meta.db

        # Change the abstract.
        self.abstract = getattr(Meta, "abstract", self.abstract)

        # Change the table name.
        if hasattr(Meta, 'table_name'):
            self.table_name = Meta.table_name

    def __repr__(self):
        return "<MetaInfo for='{}' fields={} />".format(
            self.name,
            str(self.fields)
        )


class ModelType(type):

    def __new__(cls, name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):

        # Start with a fresh meta.
        meta = Meta(name)

        # Extract some information from bases.
        for base in bases:
            if hasattr(base, '_meta'):

                # Copy the reference to a database.
                meta.db = base._meta.db

                # Copy fields.
                for field_name, field in base._meta.fields.items():
                    meta.fields[field_name] = field.copy()

        if "Meta" in attrs:
            meta.extend_from_model(attrs["Meta"])

        # Append the fields defined in the model.
        for name, value in attrs.items():
            if isinstance(value, BaseField):
                meta.fields[name] = value

        # Append the meta information to the class.
        attrs["_meta"] = meta

        model = super().__new__(cls, name, bases, attrs)

        # Add the model to the dictionary of models if is not abstract.
        if not meta.abstract:
            meta.db.models[meta.table_name] = model

        # Add a reference for the fields.
        for field in meta.fields.values():
            field.model = model

        return model

    def from_record(cls, record):
        return cls(**record)


class Database:
    """ Database instance to interact with asyncpg.
    """

    #: Keep track of all the models defined in this database.
    models: Dict[str, Type[BaseModel]]

    _model_class : Type[BaseModel]
    debug : bool = False

    conn: Any
    pool : Any

    def __init__(self, debug=False):

        self.models = {}

        # Declare the base model class.
        self._model_class = ModelType('Model', (BaseModel, ), {
            'Meta': type('Meta', (), {
                'abstract': True,
                'db': self
            })
        })

    @property
    def Model(self):
        return self._model_class

    async def create_pool(self, url : str, **kwargs):
        # Create a connection pool using asyncpg.
        self.pool = await asyncpg.create_pool(url, **kwargs)

    async def acquire(self):
        self.conn = await self.pool.acquire()

    async def release(self):
        await self.pool.release(self.conn)

    def transaction(self):
        return self.conn.transaction()

    async def create_table(self, table_name, conn=None):

        if conn is None:
            conn = self.conn

        if isinstance(table_name, ModelType):
            table_name = table_name._meta.table_name

        # Get the model.
        model = self.models[table_name]

        # Columns
        columns = []

        for field_name, field in model._meta.fields.items():

            # Resolve the constraint.
            constraint = sql.ColumnConstraint(
                not_null=field.not_null,
                unique=field.unique,
                primary_key=field.primary_key
            )

            # Resolve any dependecies.
            if isinstance(field, ForeignKeyField):
                reftable, refcolumn = field.refs()

                # Get the on_delete action.
                on_delete = None
                if isinstance(field.on_delete, Action):
                    on_delete = field.on_delete.value

                references = sql.ColumnConstraintReference(
                    reftable, refcolumn=refcolumn,
                    on_delete=on_delete
                )

                constraint.references = references

            # Append a new column.
            columns.append(sql.Column(
                field_name, field.__postgresql_type__(), constraint
            ))

        # CreateTable.
        stmt = sql.CreateTable(table_name, columns)
        return await stmt.execute(conn, debug=self.debug)

    async def create_all_tables(self, conn=None):
        # Create all the tables.

        if conn is None:
            conn = self.conn

        # Sort the models in the right order.
        models_unsorted = list(self.models.keys())
        models_sorted = []

        while len(models_unsorted) > 0:
            key = models_unsorted[0]
            deps = self.models[key]._meta.depends
            if all(_._meta.table_name in models_sorted for _ in deps):
                models_sorted.append(models_unsorted.pop(0))
            else:
                models_unsorted.append(models_unsorted.pop(0))

        # Run all the statements inside a transaction.
        async with conn.transaction():
            for table_name in models_sorted:
                await self.create_table(table_name, conn=conn)

    def select(self, model):
        # Return a partial select statement.
        return sql.PartialSelect(model)

    async def insert(self, model, conn=None):

        if conn is None:
            conn = self.conn

        # Insert statement
        stmt = sql.Insert(
            table_name=model._meta.table_name,
            values=model.values(),
            returning=model._meta.fields.keys()
        )

        record = await stmt.fetchrow(conn=conn)

        # In-place change.
        for key, value in record.items():
            model[key] = value

        return model
