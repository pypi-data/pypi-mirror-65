from typing import Dict, Optional, List, Any
from dataclasses import dataclass


class Statement:
    pass


@dataclass
class ColumnConstraintReference:
    reftable: str
    refcolumn: Optional[str] = None
    on_delete: Optional[str] = None
    on_update: Optional[str] = None

    def __str__(self):
        stmt = f"REFERENCES {self.reftable}"

        if self.refcolumn:
            stmt = f"{stmt} ({self.refcolumn})"

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
        stmt = f"{self.name} {self.data_type}"
        if self.constraint:
            stmt = f"{stmt} {self.constraint}"
        return stmt


class WhereCondition:
    def __bool__(self):
        return False


class Expression:
    def __bool__(self):
        return False


class Select(Statement):
    """ Select statement. """

    select: Expression
    where: WhereCondition
    from_items: List[Any]

    async def execute(self, conn=None):
        stmt = "SELECT"

        if self.selectable:
            stmt = f"SELECT {self.select}"

        if self.from_items:
            from_items = ", ".join(str(item) for item in self.from_item)
            stmt = f"{stmt} FROM {from_items}"

        if self.where:
            stmt = f"{stmt} WHERE {self.where}"

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

    async def execute(self, conn):

        stmt = f"INSERT INTO {self.table_name}"

        values = []

        if self.values:
            cols = []
            placeholders = []

            for i, (name, value) in enumerate(self.values.items()):
                cols.append(name)
                placeholders.append(f'${i + 1}')
                values.append(value)

            cols = ', '.join(cols)
            placeholders = ', '.join(placeholders)
            stmt = f"{stmt} ({cols}) VALUES ({placeholders})"

        if self.returning:
            returning = ', '.join(self.returning)
            stmt = f"{stmt} RETURNING ({returning})"

        return await conn.fetchrow(stmt, *values)


class CreateTable(Statement):

    name : str
    columns : List[Column]

    def __init__(self, name : str, columns : List[Column]):
        self.name = name
        self.columns = columns

    async def execute(self, conn):
        stmt = f"CREATE TABLE IF NOT EXISTS {self.name}"

        if self.columns:
            columns = ', '.join(str(col) for col in self.columns)
            stmt = f"{stmt} ({columns})"

        return await conn.execute(stmt)
