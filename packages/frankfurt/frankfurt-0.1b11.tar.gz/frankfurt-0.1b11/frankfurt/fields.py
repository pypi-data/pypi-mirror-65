from enum import Enum
from uuid import uuid4


class Action(Enum):
    NO_ACTION = "NO ACTION"
    RESTRICT = "RESTRICT"
    CASCADE = "CASCADE"
    SET_NULL = "SET NULL"
    SET_DEFAULT = "SET DEFAULT"


# Export the actions.
CASCADE = Action.CASCADE


class BaseField:

    not_null : bool = False
    unique : bool = False
    primary_key : bool = False

    __kwargs__ = [
        'not_null',
        'unique',
        'primary_key',
        'default'
    ]

    @property
    def default(self):
        if callable(self._default):
            return self._default()
        return self._default

    def __init__(self, **kwargs):

        for v in kwargs:
            if v not in self.__kwargs__:
                raise TypeError(f"Argument {v} is not needed.")

        self._copy_kwargs = kwargs.copy()

        # Can this field be null.
        if 'not_null' in kwargs:
            self.not_null = kwargs['not_null']

        # Is this field unique.
        if 'unique' in kwargs:
            self.unique = kwargs['unique']

        # Is this field a primary key?
        if 'primary_key' in kwargs:
            self.primary_key = kwargs['primary_key']

        # Add None as default if necessary.
        if not self.not_null and 'default' not in kwargs:
            self.has_default = True
            self._default = None
        elif 'default' in kwargs:
            self.has_default = True
            self._default = kwargs['default']
        else:
            self.has_default = False

    def copy(self):
        return self.__class__(**self._copy_kwargs)


class CharField(BaseField):
    """String-based field."""

    def __postgresql_type__(self):
        return f"VARCHAR({self.max_length})"

    def copy(self):
        return CharField(max_length=self.max_length, **self._copy_kwargs)

    def __init__(self, max_length: int = 256, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length


class UUIDField(BaseField):
    def __postgresql_type__(self):
        return "UUID"

    def __init__(self, **kwargs):
        if kwargs.get('primary_key', False) and 'default' not in kwargs:
            kwargs['default'] = uuid4
        super().__init__(**kwargs)


class BinaryField(BaseField):
    def __postgresql_type__(self):
        return "BYTEA"


class DateTimeField(BaseField):
    def __postgresql_type__(self):
        return "TIMESTAMPTZ"

    def __init__(self, auto_now=False, auto_now_add=False, **kwargs):
        super().__init__(**kwargs)

        # auto_now implies auto_now_add
        self.auto_now_add = auto_now_add or auto_now
        self.auto_now = auto_now

    def copy(self):
        return DateTimeField(
            auto_now=self.auto_now,
            auto_now_add=self.auto_now_add,
            **self._copy_kwargs
        )


class ForeignKeyField(BaseField):

    _to_field = None

    def __postgresql_type__(self):
        return self.to_field.__postgresql_type__()

    @property
    def to_field(self):
        self._resolve()
        return self._to_field

    def refs(self):
        reftable = self.to_field.model._meta.table_name
        refcolumn = None
        for field_name, field in self.to_field.model._meta.fields.items():
            if field == self.to_field:
                refcolumn = field_name

        return reftable, refcolumn

    def _resolve(self):

        if self._to_field is not None:
            return

        to_parts = self.to.split('.')
        table_name = to_parts[0]
        to_model = None

        # Resolve first the model.
        if table_name not in self.model._meta.db.models:
            raise Exception("ForeignKey can't be resolved.")
        to_model = self.model._meta.db.models[table_name]

        # Check if there is a field.
        if len(to_parts) > 1:
            to_field_name = to_parts[1]
            if to_field_name not in to_model._meta.fields:
                raise Exception("ForeignKey can't be resolved.")
            self.to_field = to_model._meta[to_field_name]
        else:
            for field_name, field in to_model._meta.fields.items():
                if field.primary_key:
                    self._to_field = field
                    break

        if self._to_field is None:
            raise Exception("ForeignKey can't be resolved.")

    def __init__(self, to, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.to = to
        self.on_delete = on_delete

        if isinstance(self.to, BaseField):
            self._to_field = self.to

    def copy(self):
        return self.__class__(
            to=self.to,
            on_delete=self.on_delete,
            **self._copy_kwargs
        )
