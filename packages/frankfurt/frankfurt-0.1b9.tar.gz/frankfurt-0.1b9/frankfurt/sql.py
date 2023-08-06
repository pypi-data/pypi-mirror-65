import logging
from typing import Dict, Optional, List, Any, Union
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Statement:
    pass


@dataclass
class ColumnConstraintReference:
    reftable: str
    refcolumn: Optional[str] = None
    on_delete: Optional[str] = None
    on_update: Optional[str] = None

    def __str__(self):
        stmt = f'REFERENCES "{self.reftable}"'

        if self.refcolumn:
            stmt = f'{stmt} ("{self.refcolumn}")'

        if self.on_delete:
            stmt = f'{stmt} ON DELETE {self.on_delete}'

        return stmt


@dataclass
class ColumnConstraint:
    not_null: bool = False
    primary_key: bool = False
    references: Optional[ColumnConstraintReference] = None
    unique : bool = False

    def __bool__(self):

        if self.not_null:
            return True

        if self.primary_key:
            return True

        if self.references:
            return True

        if self.unique:
            return True

        return False

    def __str__(self):

        constraints = []

        if self.not_null:
            constraints.append("NOT NULL")

        if self.unique:
            constraints.append("UNIQUE")

        if self.primary_key:
            constraints.append("PRIMARY KEY")

        if self.references:
            constraints.append(str(self.references))

        return " ".join(constraints)


@dataclass
class Column:

    name : str
    data_type : str
    constraint : Optional[ColumnConstraint] = None

    def __init__(
            self,
            name : str,
            data_type : str,
            constraint : Optional[ColumnConstraint] = None
    ):

        self.name = name
        self.data_type = data_type
        self.constraint = constraint

    def __str__(self):
        stmt = f'"{self.name}" {self.data_type}'

        if self.constraint:
            stmt = f"{stmt} {self.constraint}"
        return stmt


@dataclass
class WhereClause:
    def __bool__(self):
        return False

    def __and__(self, other):
        return WhereClauseAnd(parts=[other])


class Expression:
    def __bool__(self):
        return False


@dataclass
class WhereClauseEquality(WhereClause):
    lhs: Expression
    rhs: Expression

    def __bool__(self):
        return True

    def __str__(self):
        return f'{self.lhs} = {self.rhs}'


@dataclass
class WhereClauseAnd(WhereClause):
    parts: List[WhereClause] = field(default_factory=list)

    def __bool__(self):
        return len(self.parts) > 0

    def __str__(self):
        return " AND ".join(f'({_})' for _ in self.parts)

    def __and__(self, other):
        return WhereClauseAnd(parts=self.parts + [other])


@dataclass
class ExpressionColumnName(Expression):
    name : str

    def __bool__(self):
        return self.name != ""

    def __str__(self):
        return f'"{self.name}"'

@dataclass
class ExpressionLiteralString(Expression):
    value : str

    def __bool__(self):
        return self.value != ""

    def __str__(self):
        return  f"'{self.value}'"


class Asterisk(Expression):
    def __bool__(self):
        return True

    def __str__(self):
        return '*'


class PartialSelect:
    def __init__(self, *models):
        self.models = models
        self._where = WhereClause()

    def where(self, **kwargs):
        for name, value in kwargs.items():
            lhs = ExpressionColumnName(name=name)
            rhs = ExpressionLiteralString(value=value)
            self._where &= WhereClauseEquality(lhs=lhs, rhs=rhs)
        return self

    async def one(self, conn=None):
        #: Return one instance of a model or raise an error.

        # We need only one model.
        if len(self.models) != 1:
            raise Exception("To fetch one we need a single model.")

        #: Select all the fields.
        select = list(self.models[0]._meta.fields.keys())
        select = [ExpressionColumnName(name=name) for name in select]

        # Table name to select from.
        from_table = self.models[0]._meta.table_name

        # Create the statement.
        stmt = Select(
            select=select,
            where=self._where,
            from_items=[f'"{from_table}"']
        )

        # TODO: Add a count statement first and then a fetch.
        # Get a list of records.
        records = await stmt.fetch(conn=conn)

        if len(records) != 1:
            raise Exception("Return only one element.")

        # TODO: This should
        return self.models[0].from_record(records[0])


@dataclass
class Select(Statement):
    """ Select statement. """

    select: Union[Asterisk, List[Expression], List[str]]
    where: WhereClause
    from_items: List[Any]

    async def fetch(self, conn, debug : bool = False):
        stmt = "SELECT"

        if self.select:
            if isinstance(self.select, list):
                select = ', '.join(str(_) for _ in self.select)
            else:
                select = self.select

            stmt = f"SELECT {select}"

        if self.from_items:
            from_items = ", ".join(str(item) for item in self.from_items)
            stmt = f"{stmt} FROM {from_items}"

        if self.where:
            stmt = f"{stmt} WHERE {self.where}"

        if debug:
            logger.debug(stmt)

        return await conn.fetch(stmt)


class Insert(Statement):
    """ Insert statement. """

    table_name : str
    values : Dict[str, Any]
    returning: List[str]

    def __init__(
            self, table_name : str,
            values : Optional[Dict[str, Any]] = None,
            returning : Optional[List[str]] = None
    ):

        self.table_name = table_name
        self.values = values if values is not None else {}
        self.returning = returning if returning is not None else []

    async def execute(self, conn, debug : bool = False):

        stmt = f'INSERT INTO "{self.table_name}"'

        values = []

        if self.values:
            cols = []
            placeholders = []

            for i, (name, value) in enumerate(self.values.items()):
                cols.append(f'"{name}"')
                placeholders.append(f'${i + 1}')
                values.append(value)

            cols = ', '.join(cols)
            placeholders = ', '.join(placeholders)
            stmt = f"{stmt} ({cols}) VALUES ({placeholders})"

        if self.returning:
            returning = ', '.join(f'"{name}"' for name in self.returning)
            stmt = f"{stmt} RETURNING ({returning})"

        if debug:
            logger.debug(stmt)

        return await conn.fetchrow(stmt, *values)


class CreateTable(Statement):

    name : str
    columns : List[Column]

    def __init__(self, name : str, columns : List[Column]):
        self.name = name
        self.columns = columns

    async def execute(self, conn, debug : bool = False):
        stmt = f'CREATE TABLE IF NOT EXISTS "{self.name}"'

        if self.columns:
            columns = ', '.join(str(col) for col in self.columns)
            stmt = f"{stmt} ({columns})"

        if debug:
            logger.debug(stmt)

        return await conn.execute(stmt)
