from typing import Tuple, Type, Dict, Any, List

import asyncpg

from frankfurt.fields import BaseField, ForeignKeyField, Action
import frankfurt.sql


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

    def values(self):
        return self.__data__.copy()

    async def save(self, conn=None):
        # Use the methods in db.
        self._meta.db.insert(self, conn=conn)


class HasNotFieldTypeError(TypeError):
    def __init__(self, field_name, cls):
        super().__init__("Model {} has not field {}".format(
            cls.__class__.__name__, field_name
        ))
