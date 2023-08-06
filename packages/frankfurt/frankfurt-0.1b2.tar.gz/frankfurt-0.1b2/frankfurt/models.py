from typing import Tuple, Type, Dict, Any, List

from frankfurt.fields import BaseField, ForeignKeyField, Action
import frankfurt.sql


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


class BaseModel:
    def __init__(self, **kwargs):

        # Save the value of the fields in this dict
        self.__data__ = {}

        # Check for the kwargs in the fields.
        for name, value in kwargs.items():
            if name in self._meta.fields:
                self.__data__[name] = value
            else:
                raise HasNotFieldTypeError(name, self)

        # Continue with default values.
        for field_name, field in self._meta.fields.items():
            if field_name not in self.__data__:
                if field.has_default:
                    self.__data__[field_name] = field.default

        # Check for not nulls (or maybe types?)
        for field_name, field in self._meta.fields.items():
            if field_name in self.__data__:
                if field.not_null and self.__data__[field_name] is None:
                    raise TypeError(
                        "Field {} cannot be null (None)".format(field_name)
                    )

    def __setitem__(self, key : str, value):
        if key not in self._meta.fields:
            msg = "Model {} has not field {}.".format(self._meta.name, key)
            raise KeyError(msg)
        self.__data__[key] = value

    def __getitem__(self, key : str):
        if key not in self._meta.fields:
            msg = "Model {} has not field {}.".format(self._meta.name, key)
            raise KeyError(msg)

        if key not in self.__data__:
            raise KeyError("Field {} has no value.".format(key))

        return self.__data__[key]

    async def save(self, conn=None):
        ins = frankfurt.sql.Insert(
            table_name=self._meta.table_name,
            values=self.__data__,
            returning=self._meta.fields.keys()
        )

        # Insert and get the record.
        record = await ins.execute(conn=conn)

        for key, value in record.items():
            self.__data__[key] = value


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


class Database:
    models : Dict[str, Type[BaseModel]]
    model_class : Type[BaseModel]

    def __init__(self):

        self.models = {}

        # Declare the base model class.
        self.model_class = ModelType('BaseModel', (BaseModel, ), {
            'Meta': type('Meta', (), {
                'abstract': True,
                'db': self
            })
        })

    @property
    def Model(self):
        return self.model_class

    async def create_table(self, table_name, conn=None):

        if isinstance(table_name, ModelType):
            table_name = table_name._meta.table_name

        # Get the model.
        model = self.models[table_name]

        # Columns
        columns = []

        for field_name, field in model._meta.fields.items():

            # Resolve the constraint.
            constraint = frankfurt.sql.ColumnConstraint(
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

                references = frankfurt.sql.ColumnConstraintReference(
                    reftable, refcolumn=refcolumn,
                    on_delete=on_delete
                )

                constraint.references = references

            # Append a new column.
            columns.append(frankfurt.sql.Column(
                field_name, field.__postgresql_type__(), constraint
            ))

        # CreateTable.
        stmt = frankfurt.sql.CreateTable(table_name, columns)
        return await stmt.execute(conn)

    async def create_all_tables(self, conn=None):
        # Create all the tables.

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


class HasNotFieldTypeError(TypeError):
    def __init__(self, field_name, cls):
        super().__init__("Model {} has not field {}".format(
            cls.__class__.__name__, field_name
        ))


db = Database()

Model = db.Model
