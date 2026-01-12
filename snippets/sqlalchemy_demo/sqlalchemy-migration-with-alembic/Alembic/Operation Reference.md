---
author: null
description: null
published: null
source: https://alembic.sqlalchemy.org/en/latest/ops.html
tags:
- Alembic
- SQLAlchemy-Migration
title: Operation Reference — Alembic 1.17.2 documentation
---

## Operation Reference

This file provides documentation on Alembic migration directives.

The directives here are used within user-defined migration files, within the `upgrade()` and `downgrade()` functions, as well as any functions further invoked by those.

All directives exist as methods on a class called . When migration scripts are run, this object is made available to the script via the `alembic.op` datamember, which is a *proxy* to an actual instance of . Currently, `alembic.op` is a real Python module, populated with individual proxies for each method on , so symbols can be imported safely from the `alembic.op` namespace.

The system is also fully extensible. See [Operation Plugins](https://alembic.sqlalchemy.org/en/latest/api/operations.html#operation-plugins) for details on this.

A key design philosophy to the [Operation Directives](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic-operations-toplevel) methods is that to the greatest degree possible, they internally generate the appropriate SQLAlchemy metadata, typically involving [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") and [`Constraint`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint "(in SQLAlchemy v2.0)") objects. This so that migration instructions can be given in terms of just the string names and/or flags involved. The exceptions to this rule include the and directives, which require full [`Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column "(in SQLAlchemy v2.0)") objects, though the table metadata is still generated here.

The functions here all require that a [`MigrationContext`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext") has been configured within the `env.py` script first, which is typically via [`EnvironmentContext.configure()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure "alembic.runtime.environment.EnvironmentContext.configure"). Under normal circumstances they are called from an actual migration script, which itself would be invoked by the [`EnvironmentContext.run_migrations()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.run_migrations "alembic.runtime.environment.EnvironmentContext.run_migrations") method.

*class* alembic.operations.AbstractOperations [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.AbstractOperations "Link to this definition")

Base class for and .

See for full list of members

*class* alembic.operations.Operations (*migration\_context:[MigrationContext](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext")*, *impl:BatchOperationsImpl | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations "Link to this definition")

Define high level migration operations.

Each operation corresponds to some schema migration operation, executed against a particular [`MigrationContext`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext") which in turn represents connectivity to a database, or a file output stream.

While is normally configured as part of the [`EnvironmentContext.run_migrations()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.run_migrations "alembic.runtime.environment.EnvironmentContext.run_migrations") method called from an `env.py` script, a standalone instance can be made for use cases external to regular Alembic migrations by passing in a [`MigrationContext`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext"):

```
from alembic.migration import MigrationContext
from alembic.operations import Operations

conn = myengine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

op.alter_column("t", "c", nullable=True)
```

Note that as of 0.8, most of the methods on this class are produced dynamically using the method.

Construct a new

Parameters:

**migration\_context** – a [`MigrationContext`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext") instance.

add\_column (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *column:Column \[Any\]*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *if\_not\_exists:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.add_column "Link to this definition")

Issue an “add column” instruction using the current migration context.

e.g.:

```
from alembic import op
from sqlalchemy import Column, String

op.add_column("organization", Column("name", String()))
```

The method typically corresponds to the SQL command “ALTER TABLE… ADD COLUMN”. Within the scope of this command, the column’s name, datatype, nullability, and optional server-generated defaults may be indicated.

Note

With the exception of NOT NULL constraints or single-column FOREIGN KEY constraints, other kinds of constraints such as PRIMARY KEY, UNIQUE or CHECK constraints **cannot** be generated using this method; for these constraints, refer to operations such as and. In particular, the following [`Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column "(in SQLAlchemy v2.0)") parameters are **ignored**:

- `primary_key` - SQL databases typically do not support an ALTER operation that can add individual columns one at a time to an existing primary key constraint, therefore it’s less ambiguous to use the method, which assumes no existing primary key constraint is present.
- `unique` - use the method
- `index` - use the method

The provided [`Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column "(in SQLAlchemy v2.0)") object may include a [`ForeignKey`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey "(in SQLAlchemy v2.0)") constraint directive, referencing a remote table name. For this specific type of constraint, Alembic will automatically emit a second ALTER statement in order to add the single-column FOREIGN KEY constraint separately:

```
from alembic import op
from sqlalchemy import Column, INTEGER, ForeignKey

op.add_column(
    "organization",
    Column("account_id", INTEGER, ForeignKey("accounts.id")),
)
```

The column argument passed to is a [`Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column "(in SQLAlchemy v2.0)") construct, used in the same way it’s used in SQLAlchemy. In particular, values or functions to be indicated as producing the column’s default value on the database side are specified using the `server_default` parameter, and not `default` which only specifies Python-side defaults:

```
from alembic import op
from sqlalchemy import Column, TIMESTAMP, func

# specify "DEFAULT NOW" along with the column add
op.add_column(
    "account",
    Column("timestamp", TIMESTAMP, server_default=func.now()),
)
```

Parameters:

- **table\_name** – String name of the parent table.
- **column** – a [`sqlalchemy.schema.Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column "(in SQLAlchemy v2.0)") object representing the new column.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **if\_not\_exists** –
	If True, adds IF NOT EXISTS operator when creating the new column for compatible dialects

alter\_column (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *column\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *nullable:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | Literal \[False\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= False*, *server\_default:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | Identity | Computed | TextClause | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= False*, *new\_column\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *type\_:TypeEngine \[Any\] | Type \[TypeEngine \[Any\]\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *existing\_type:TypeEngine \[Any\] | Type \[TypeEngine \[Any\]\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *existing\_server\_default:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | Identity | Computed | TextClause | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= False*, *existing\_nullable:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *existing\_comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:Any*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.alter_column "Link to this definition")

Issue an “alter column” instruction using the current migration context.

Generally, only that aspect of the column which is being changed, i.e. name, type, nullability, default, needs to be specified. Multiple changes can also be specified at once and the backend should “do the right thing”, emitting each change either separately or together as the backend allows.

MySQL has special requirements here, since MySQL cannot ALTER a column without a full specification. When producing MySQL-compatible migration files, it is recommended that the `existing_type`,`existing_server_default`, and `existing_nullable` parameters be present, if not being altered.

Type changes which are against the SQLAlchemy “schema” types [`Boolean`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean "(in SQLAlchemy v2.0)") and [`Enum`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum "(in SQLAlchemy v2.0)") may also add or drop constraints which accompany those types on backends that don’t support them natively. The `existing_type` argument is used in this case to identify and remove a previous constraint that was bound to the type object.

Parameters:

- **table\_name** – string name of the target table.
- **column\_name** – string name of the target column, as it exists before the operation begins.
- **nullable** – Optional; specify `True` or `False` to alter the column’s nullability.
- **server\_default** – Optional; specify a string SQL expression, [`text()`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text "(in SQLAlchemy v2.0)"), or [`DefaultClause`](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.DefaultClause "(in SQLAlchemy v2.0)") to indicate an alteration to the column’s default value. Set to `None` to have the default removed.
- **comment** – optional string text of a new comment to add to the column.
- **new\_column\_name** – Optional; specify a string name here to indicate the new name within a column rename operation.
- **type\_** – Optional; a [`TypeEngine`](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine "(in SQLAlchemy v2.0)") type object to specify a change to the column’s type. For SQLAlchemy types that also indicate a constraint (i.e.[`Boolean`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean "(in SQLAlchemy v2.0)"), [`Enum`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum "(in SQLAlchemy v2.0)")), the constraint is also generated.
- **autoincrement** – set the `AUTO_INCREMENT` flag of the column; currently understood by the MySQL dialect.
- **existing\_type** – Optional; a [`TypeEngine`](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine "(in SQLAlchemy v2.0)") type object to specify the previous type. This is required for all MySQL column alter operations that don’t otherwise specify a new type, as well as for when nullability is being changed on a SQL Server column. It is also used if the type is a so-called SQLAlchemy “schema” type which may define a constraint (i.e.[`Boolean`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean "(in SQLAlchemy v2.0)"),[`Enum`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum "(in SQLAlchemy v2.0)")), so that the constraint can be dropped.
- **existing\_server\_default** – Optional; The existing default value of the column. Required on MySQL if an existing default is not being changed; else MySQL removes the default.
- **existing\_nullable** – Optional; the existing nullability of the column. Required on MySQL if the existing nullability is not being changed; else MySQL sets this to NULL.
- **existing\_autoincrement** – Optional; the existing autoincrement of the column. Used for MySQL’s system of altering a column that specifies `AUTO_INCREMENT`.
- **existing\_comment** – string text of the existing comment on the column to be maintained. Required on MySQL if the existing comment on the column is not being changed.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **postgresql\_using** – String argument which will indicate a SQL expression to render within the Postgresql-specific USING clause within ALTER COLUMN. This string is taken directly as raw SQL which must explicitly include any necessary quoting or escaping of tokens within the expression.

batch\_alter\_table (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *recreate:Literal \['auto','always','never'\] \= 'auto'*, *partial\_reordering:[list](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") \[[tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),...\]\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *copy\_from:Table | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *table\_args:Tuple \[Any,...\] \= ()*, *table\_kwargs:Mapping \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),Any\] \= {}*, *reflect\_args:Tuple \[Any,...\] \= ()*, *reflect\_kwargs:Mapping \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),Any\] \= {}*, *naming\_convention:Dict \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → Iterator \[\] [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.batch_alter_table "Link to this definition")

Invoke a series of per-table migrations in batch.

Batch mode allows a series of operations specific to a table to be syntactically grouped together, and allows for alternate modes of table migration, in particular the “recreate” style of migration required by SQLite.

“recreate” style is as follows:

1. A new table is created with the new specification, based on the migration directives within the batch, using a temporary name.
2. the data copied from the existing table to the new table.
3. the existing table is dropped.
4. the new table is renamed to the existing table name.

The directive by default will only use “recreate” style on the SQLite backend, and only if directives are present which require this form, e.g. anything other than `add_column()`. The batch operation on other backends will proceed using standard ALTER TABLE operations.

The method is used as a context manager, which returns an instance of ; this object is the same as except that table names and schema names are omitted. E.g.:

```
with op.batch_alter_table("some_table") as batch_op:
    batch_op.add_column(Column("foo", Integer))
    batch_op.drop_column("bar")
```

The operations within the context manager are invoked at once when the context is ended. When run against SQLite, if the migrations include operations not supported by SQLite’s ALTER TABLE, the entire table will be copied to a new one with the new specification, moving all data across as well.

The copy operation by default uses reflection to retrieve the current structure of the table, and therefore in this mode requires that the migration is run in “online” mode. The `copy_from` parameter may be passed which refers to an existing `Table` object, which will bypass this reflection step.

Note

The table copy operation will currently not copy CHECK constraints, and may not copy UNIQUE constraints that are unnamed, as is possible on SQLite. See the section [Dealing with Constraints](https://alembic.sqlalchemy.org/en/latest/batch.html#sqlite-batch-constraints) for workarounds.

Parameters:

- **table\_name** – name of table
- **schema** – optional schema name.
- **recreate** – under what circumstances the table should be recreated. At its default of `"auto"`, the SQLite dialect will recreate the table if any operations other than `add_column()`,`create_index()`, or `drop_index()` are present. Other options include `"always"` and `"never"`.
- **copy\_from** –
	optional [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object that will act as the structure of the table being copied. If omitted, table reflection is used to retrieve the structure of the table.
	See also
	[Working in Offline Mode](https://alembic.sqlalchemy.org/en/latest/batch.html#batch-offline-mode)
- **reflect\_args** – a sequence of additional positional arguments that will be applied to the table structure being reflected / copied; this may be used to pass column and constraint overrides to the table that will be reflected, in lieu of passing the whole [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") using.
- **reflect\_kwargs** – a dictionary of additional keyword arguments that will be applied to the table structure being copied; this may be used to pass additional table and reflection options to the table that will be reflected, in lieu of passing the whole [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") using.
- **table\_args** – a sequence of additional positional arguments that will be applied to the new [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") when created, in addition to those copied from the source table. This may be used to provide additional constraints such as CHECK constraints that may not be reflected.
- **table\_kwargs** – a dictionary of additional keyword arguments that will be applied to the new [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") when created, in addition to those copied from the source table. This may be used to provide for additional table options that may not be reflected.
- **naming\_convention** –
	a naming convention dictionary of the form described at [Integration of Naming Conventions into Operations, Autogenerate](https://alembic.sqlalchemy.org/en/latest/naming.html#autogen-naming-conventions) which will be applied to the [`MetaData`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData "(in SQLAlchemy v2.0)") during the reflection process. This is typically required if one wants to drop SQLite constraints, as these constraints will not have names when reflected on this backend. Requires SQLAlchemy **0.9.4** or greater.
	See also
	[Dropping Unnamed or Named Foreign Key Constraints](https://alembic.sqlalchemy.org/en/latest/batch.html#dropping-sqlite-foreign-keys)
- **partial\_reordering** –
	a list of tuples, each suggesting a desired ordering of two or more columns in the newly created table. Requires that is set to `"always"`. Examples, given a table with columns “a”, “b”, “c”, and “d”:
	Specify the order of all columns:
	```
	with op.batch_alter_table(
	    "some_table",
	    recreate="always",
	    partial_reordering=[("c", "d", "a", "b")],
	) as batch_op:
	    pass
	```
	Ensure “d” appears before “c”, and “b”, appears before “a”:
	```
	with op.batch_alter_table(
	    "some_table",
	    recreate="always",
	    partial_reordering=[("d", "c"), ("b", "a")],
	) as batch_op:
	    pass
	```
	The ordering of columns not included in the partial\_reordering set is undefined. Therefore it is best to specify the complete ordering of all columns for best results.

Note

batch mode requires SQLAlchemy 0.8 or above.

See also

[Running “Batch” Migrations for SQLite and Other Databases](https://alembic.sqlalchemy.org/en/latest/batch.html#batch-migrations)

bulk\_insert (*table:Table | TableClause*, *rows:List \[Dict \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),Any\]\]*, *\**, *multiinsert:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") \= True*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.bulk_insert "Link to this definition")

Issue a “bulk insert” operation using the current migration context.

This provides a means of representing an INSERT of multiple rows which works equally well in the context of executing on a live connection as well as that of generating a SQL script. In the case of a SQL script, the values are rendered inline into the statement.

e.g.:

```
from alembic import op
from datetime import date
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date

# Create an ad-hoc table to use for the insert statement.
accounts_table = table(
    "account",
    column("id", Integer),
    column("name", String),
    column("create_date", Date),
)

op.bulk_insert(
    accounts_table,
    [
        {
            "id": 1,
            "name": "John Smith",
            "create_date": date(2010, 10, 5),
        },
        {
            "id": 2,
            "name": "Ed Williams",
            "create_date": date(2007, 5, 27),
        },
        {
            "id": 3,
            "name": "Wendy Jones",
            "create_date": date(2008, 8, 15),
        },
    ],
)
```

When using –sql mode, some datatypes may not render inline automatically, such as dates and other special types. When this issue is present, may be used:

```
op.bulk_insert(
    accounts_table,
    [
        {
            "id": 1,
            "name": "John Smith",
            "create_date": op.inline_literal("2010-10-05"),
        },
        {
            "id": 2,
            "name": "Ed Williams",
            "create_date": op.inline_literal("2007-05-27"),
        },
        {
            "id": 3,
            "name": "Wendy Jones",
            "create_date": op.inline_literal("2008-08-15"),
        },
    ],
    multiinsert=False,
)
```

When using in conjunction with, in order for the statement to work in “online” (e.g. non –sql) mode, theflag should be set to `False`, which will have the effect of individual INSERT statements being emitted to the database, each with a distinct VALUES clause, so that the “inline” values can still be rendered, rather than attempting to pass the values as bound parameters.

Parameters:

- **table** – a table object which represents the target of the INSERT.
- **rows** – a list of dictionaries indicating rows.
- **multiinsert** – when at its default of True and –sql mode is not enabled, the INSERT statement will be executed using “executemany()” style, where all elements in the list of dictionaries are passed as bound parameters in a single list. Setting this to False results in individual INSERT statements being emitted per parameter set, and is needed in those cases where non-literal values are present in the parameter sets.

create\_check\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *condition:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | ColumnElement \[[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")\] | TextClause*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:Any*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_check_constraint "Link to this definition")

Issue a “create check constraint” instruction using the current migration context.

e.g.:

```
from alembic import op
from sqlalchemy.sql import column, func

op.create_check_constraint(
    "ck_user_name_len",
    "user",
    func.len(column("name")) > 5,
)
```

CHECK constraints are usually against a SQL expression, so ad-hoc table metadata is usually needed. The function will convert the given arguments into a [`sqlalchemy.schema.CheckConstraint`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint "(in SQLAlchemy v2.0)") bound to an anonymous table in order to emit the CREATE statement.

Parameters:

- **name** – Name of the check constraint. The name is necessary so that an ALTER statement can be emitted. For setups that use an automated naming scheme such as that described at [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions "(in SQLAlchemy v2.0)"),`name` here can be `None`, as the event listener will apply the name to the constraint object when it is associated with the table.
- **table\_name** – String name of the source table.
- **condition** – SQL expression that’s the condition of the constraint. Can be a string or SQLAlchemy expression language structure.
- **deferrable** – optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.
- **initially** – optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").

create\_exclude\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\* elements:Any*, *\*\* kw:Any*) → Table | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_exclude_constraint "Link to this definition")

Issue an alter to create an EXCLUDE constraint using the current migration context.

Note

This method is Postgresql specific, and additionally requires at least SQLAlchemy 1.0.

e.g.:

```
from alembic import op

op.create_exclude_constraint(
    "user_excl",
    "user",
    ("period", "&&"),
    ("group", "="),
    where=("group != 'some group'"),
)
```

Note that the expressions work the same way as that of the `ExcludeConstraint` object itself; if plain strings are passed, quoting rules must be applied manually.

Parameters:

- **name** – Name of the constraint.
- **table\_name** – String name of the source table.
- **elements** – exclude conditions.
- **where** – SQL expression or SQL string with optional WHERE clause.
- **deferrable** – optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.
- **initially** – optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.
- **schema** – Optional schema name to operate within.

create\_foreign\_key (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *source\_table:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *referent\_table:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *local\_cols:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *remote\_cols:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *\**, *onupdate:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *ondelete:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *deferrable:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *initially:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *match:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *source\_schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *referent\_schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* dialect\_kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_foreign_key "Link to this definition")

Issue a “create foreign key” instruction using the current migration context.

e.g.:

```
from alembic import op

op.create_foreign_key(
    "fk_user_address",
    "address",
    "user",
    ["user_id"],
    ["id"],
)
```

This internally generates a [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object containing the necessary columns, then generates a new [`ForeignKeyConstraint`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint "(in SQLAlchemy v2.0)") object which it then associates with the [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)"). Any event listeners associated with this action will be fired off normally. The [`AddConstraint`](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.AddConstraint "(in SQLAlchemy v2.0)") construct is ultimately used to generate the ALTER statement.

Parameters:

- **constraint\_name** – Name of the foreign key constraint. The name is necessary so that an ALTER statement can be emitted. For setups that use an automated naming scheme such as that described at [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions "(in SQLAlchemy v2.0)"),`name` here can be `None`, as the event listener will apply the name to the constraint object when it is associated with the table.
- **source\_table** – String name of the source table.
- **referent\_table** – String name of the destination table.
- **local\_cols** – a list of string column names in the source table.
- **remote\_cols** – a list of string column names in the remote table.
- **onupdate** – Optional string. If set, emit ON UPDATE <value> when issuing DDL for this constraint. Typical values include CASCADE, DELETE and RESTRICT.
- **ondelete** – Optional string. If set, emit ON DELETE <value> when issuing DDL for this constraint. Typical values include CASCADE, DELETE and RESTRICT.
- **deferrable** – optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.
- **source\_schema** – Optional schema name of the source table.
- **referent\_schema** – Optional schema name of the destination table.

create\_index (*index\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *columns:Sequence \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | TextClause | ColumnElement \[Any\]\]*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *unique:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") \= False*, *if\_not\_exists:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:Any*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_index "Link to this definition")

Issue a “create index” instruction using the current migration context.

e.g.:

```
from alembic import op

op.create_index("ik_test", "t1", ["foo", "bar"])
```

Functional indexes can be produced by using the [`sqlalchemy.sql.expression.text()`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text "(in SQLAlchemy v2.0)") construct:

```
from alembic import op
from sqlalchemy import text

op.create_index("ik_test", "t1", [text("lower(foo)")])
```

Parameters:

- **index\_name** – name of the index.
- **table\_name** – name of the owning table.
- **columns** – a list consisting of string column names and/or [`text()`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text "(in SQLAlchemy v2.0)") constructs.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **unique** – If True, create a unique index.
- **quote** – Force quoting of this column’s name on or off, corresponding to `True` or `False`. When left at its default of `None`, the column identifier will be quoted according to whether the name is case sensitive (identifiers with at least one upper case character are treated as case sensitive), or if it’s a reserved word. This flag is only needed to force quoting of a reserved word which is not known by the SQLAlchemy dialect.
- **if\_not\_exists** –
	If True, adds IF NOT EXISTS operator when creating the new index.
- **\*\*kw** – Additional keyword arguments not mentioned above are dialect specific, and passed in the form `<dialectname>_<argname>`. See the documentation regarding an individual dialect at [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html#dialect-toplevel "(in SQLAlchemy v2.0)") for detail on documented arguments.

create\_primary\_key (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *columns:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_primary_key "Link to this definition")

Issue a “create primary key” instruction using the current migration context.

e.g.:

```
from alembic import op

op.create_primary_key("pk_my_table", "my_table", ["id", "version"])
```

This internally generates a [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object containing the necessary columns, then generates a new [`PrimaryKeyConstraint`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "(in SQLAlchemy v2.0)") object which it then associates with the [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)"). Any event listeners associated with this action will be fired off normally. The [`AddConstraint`](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.AddConstraint "(in SQLAlchemy v2.0)") construct is ultimately used to generate the ALTER statement.

Parameters:

- **constraint\_name** – Name of the primary key constraint. The name is necessary so that an ALTER statement can be emitted. For setups that use an automated naming scheme such as that described at [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions "(in SQLAlchemy v2.0)") `name` here can be `None`, as the event listener will apply the name to the constraint object when it is associated with the table.
- **table\_name** – String name of the target table.
- **columns** – a list of string column names to be applied to the primary key constraint.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").

create\_table (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\* columns:SchemaItem*, *if\_not\_exists:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:Any*) → Table [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_table "Link to this definition")

Issue a “create table” instruction using the current migration context.

This directive receives an argument list similar to that of the traditional [`sqlalchemy.schema.Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") construct, but without the metadata:

```
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column
from alembic import op

op.create_table(
    "account",
    Column("id", INTEGER, primary_key=True),
    Column("name", VARCHAR(50), nullable=False),
    Column("description", NVARCHAR(200)),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
)
```

Note that accepts [`Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column "(in SQLAlchemy v2.0)") constructs directly from the SQLAlchemy library. In particular, default values to be created on the database side are specified using the `server_default` parameter, and not `default` which only specifies Python-side defaults:

```
from alembic import op
from sqlalchemy import Column, TIMESTAMP, func

# specify "DEFAULT NOW" along with the "timestamp" column
op.create_table(
    "account",
    Column("id", INTEGER, primary_key=True),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
)
```

The function also returns a newly created [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object, corresponding to the table specification given, which is suitable for immediate SQL operations, in particular:

```
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column
from alembic import op

account_table = op.create_table(
    "account",
    Column("id", INTEGER, primary_key=True),
    Column("name", VARCHAR(50), nullable=False),
    Column("description", NVARCHAR(200)),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
)

op.bulk_insert(
    account_table,
    [
        {"name": "A1", "description": "account 1"},
        {"name": "A2", "description": "account 2"},
    ],
)
```

Parameters:

- **table\_name** – Name of the table
- **\*columns** – collection of [`Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column "(in SQLAlchemy v2.0)") objects within the table, as well as optional [`Constraint`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint "(in SQLAlchemy v2.0)") objects and [`Index`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index "(in SQLAlchemy v2.0)") objects.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **if\_not\_exists** –
	If True, adds IF NOT EXISTS operator when creating the new table.
- **\*\*kw** – Other keyword arguments are passed to the underlying [`sqlalchemy.schema.Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object created for the command.

Returns:

the [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object corresponding to the parameters given.

create\_table\_comment (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *\**, *existing\_comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_table_comment "Link to this definition")

Emit a COMMENT ON operation to set the comment for a table.

Parameters:

- **table\_name** – string name of the target table.
- **comment** – string value of the comment being registered against the specified table.
- **existing\_comment** – String value of a comment already registered on the specified table, used within autogenerate so that the operation is reversible, but not required for direct use.

See also

create\_unique\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *columns:[Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.create_unique_constraint "Link to this definition")

Issue a “create unique constraint” instruction using the current migration context.

e.g.:

```
from alembic import op
op.create_unique_constraint("uq_user_name", "user", ["name"])
```

This internally generates a [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object containing the necessary columns, then generates a new [`UniqueConstraint`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint "(in SQLAlchemy v2.0)") object which it then associates with the [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)"). Any event listeners associated with this action will be fired off normally. The [`AddConstraint`](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.AddConstraint "(in SQLAlchemy v2.0)") construct is ultimately used to generate the ALTER statement.

Parameters:

- **name** – Name of the unique constraint. The name is necessary so that an ALTER statement can be emitted. For setups that use an automated naming scheme such as that described at [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions "(in SQLAlchemy v2.0)"),`name` here can be `None`, as the event listener will apply the name to the constraint object when it is associated with the table.
- **table\_name** – String name of the source table.
- **columns** – a list of string column names in the source table.
- **deferrable** – optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.
- **initially** – optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").

drop\_column (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *column\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.drop_column "Link to this definition")

Issue a “drop column” instruction using the current migration context.

e.g.:

```
drop_column("organization", "account_id")
```

Parameters:

- **table\_name** – name of table
- **column\_name** – name of column
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **if\_exists** –
	If True, adds IF EXISTS operator when dropping the new column for compatible dialects
- **mssql\_drop\_check** – Optional boolean. When `True`, on Microsoft SQL Server only, first drop the CHECK constraint on the column using a SQL-script-compatible block that selects into a @variable from sys.check\_constraints, then exec’s a separate DROP CONSTRAINT for that constraint.
- **mssql\_drop\_default** – Optional boolean. When `True`, on Microsoft SQL Server only, first drop the DEFAULT constraint on the column using a SQL-script-compatible block that selects into a @variable from sys.default\_constraints, then exec’s a separate DROP CONSTRAINT for that default.
- **mssql\_drop\_foreign\_key** – Optional boolean. When `True`, on Microsoft SQL Server only, first drop a single FOREIGN KEY constraint on the column using a SQL-script-compatible block that selects into a @variable from sys.foreign\_keys/sys.foreign\_key\_columns, then exec’s a separate DROP CONSTRAINT for that default. Only works if the column has exactly one FK constraint which refers to it, at the moment.

drop\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *type\_:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *if\_exists:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.drop_constraint "Link to this definition")

Drop a constraint of the given name, typically via DROP CONSTRAINT.

Parameters:

- **constraint\_name** – name of the constraint.
- **table\_name** – table name.
- **type\_** – optional, required on MySQL. can be ‘foreignkey’, ‘primary’, ‘unique’, or ‘check’.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **if\_exists** –
	If True, adds IF EXISTS operator when dropping the constraint

drop\_index (*index\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *if\_exists:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.drop_index "Link to this definition")

Issue a “drop index” instruction using the current migration context.

e.g.:

```
drop_index("accounts")
```

Parameters:

- **index\_name** – name of the index.
- **table\_name** – name of the owning table. Some backends such as Microsoft SQL Server require this.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **if\_exists** –
	If True, adds IF EXISTS operator when dropping the index.
- **\*\*kw** – Additional keyword arguments not mentioned above are dialect specific, and passed in the form `<dialectname>_<argname>`. See the documentation regarding an individual dialect at [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html#dialect-toplevel "(in SQLAlchemy v2.0)") for detail on documented arguments.

drop\_table (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *if\_exists:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.drop_table "Link to this definition")

Issue a “drop table” instruction using the current migration context.

e.g.:

```
drop_table("accounts")
```

Parameters:

- **table\_name** – Name of the table
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").
- **if\_exists** –
	If True, adds IF EXISTS operator when dropping the table.
- **\*\*kw** – Other keyword arguments are passed to the underlying [`sqlalchemy.schema.Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") object created for the command.

drop\_table\_comment (*table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *existing\_comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.drop_table_comment "Link to this definition")

Issue a “drop table comment” operation to remove an existing comment set on a table.

Parameters:

- **table\_name** – string name of the target table.
- **existing\_comment** – An optional string value of a comment already registered on the specified table.

See also

execute (*sqltext:Executable | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *execution\_options:[dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),Any\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.execute "Link to this definition")

Execute the given SQL using the current migration context.

The given SQL can be a plain string, e.g.:

```
op.execute("INSERT INTO table (foo) VALUES ('some value')")
```

Or it can be any kind of Core SQL Expression construct, such as below where we use an update construct:

```
from sqlalchemy.sql import table, column
from sqlalchemy import String
from alembic import op

account = table("account", column("name", String))
op.execute(
    account.update()
    .where(account.c.name == op.inline_literal("account 1"))
    .values({"name": op.inline_literal("account 2")})
)
```

Above, we made use of the SQLAlchemy [`sqlalchemy.sql.expression.table()`](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table "(in SQLAlchemy v2.0)") and [`sqlalchemy.sql.expression.column()`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column "(in SQLAlchemy v2.0)") constructs to make a brief, ad-hoc table construct just for our UPDATE statement. A full [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") construct of course works perfectly fine as well, though note it’s a recommended practice to at least ensure the definition of a table is self-contained within the migration script, rather than imported from a module that may break compatibility with older migrations.

In a SQL script context, the statement is emitted directly to the output stream. There is *no* return result, however, as this function is oriented towards generating a change script that can run in “offline” mode. Additionally, parameterized statements are discouraged here, as they *will not work* in offline mode. Above, we use where parameters are to be used.

For full interaction with a connected database where parameters can also be used normally, use the “bind” available from the context:

```
from alembic import op

connection = op.get_bind()

connection.execute(
    account.update()
    .where(account.c.name == "account 1")
    .values({"name": "account 2"})
)
```

Additionally, when passing the statement as a plain string, it is first coerced into a [`sqlalchemy.sql.expression.text()`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text "(in SQLAlchemy v2.0)") construct before being passed along. In the less likely case that the literal SQL string contains a colon, it must be escaped with a backslash, as:

```
op.execute(r"INSERT INTO table (foo) VALUES ('\:colon_value')")
```

Parameters:

**sqltext** – Any legal SQLAlchemy expression, including:

- a string
- a [`sqlalchemy.sql.expression.text()`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text "(in SQLAlchemy v2.0)") construct.
- a [`sqlalchemy.sql.expression.insert()`](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert "(in SQLAlchemy v2.0)") construct.
- a [`sqlalchemy.sql.expression.update()`](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update "(in SQLAlchemy v2.0)") construct.
- a [`sqlalchemy.sql.expression.delete()`](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete "(in SQLAlchemy v2.0)") construct.
- Any “executable” described in SQLAlchemy Core documentation, noting that no result set is returned.

Note

when passing a plain string, the statement is coerced into a [`sqlalchemy.sql.expression.text()`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text "(in SQLAlchemy v2.0)") construct. This construct considers symbols with colons, e.g. `:foo` to be bound parameters. To avoid this, ensure that colon symbols are escaped, e.g.`\:foo`.

Parameters:

**execution\_options** – Optional dictionary of execution options, will be passed to [`sqlalchemy.engine.Connection.execution_options()`](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options "(in SQLAlchemy v2.0)").

f (*name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*) → conv [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.f "Link to this definition")

Indicate a string name that has already had a naming convention applied to it.

This feature combines with the SQLAlchemy `naming_convention` feature to disambiguate constraint names that have already had naming conventions applied to them, versus those that have not. This is necessary in the case that the `"%(constraint_name)s"` token is used within a naming convention, so that it can be identified that this particular name should remain fixed.

If the is used on a constraint, the naming convention will not take effect:

```
op.add_column("t", "x", Boolean(name=op.f("ck_bool_t_x")))
```

Above, the CHECK constraint generated will have the name `ck_bool_t_x` regardless of whether or not a naming convention is in use.

Alternatively, if a naming convention is in use, and ‘f’ is not used, names will be converted along conventions. If the `target_metadata` contains the naming convention `{"ck": "ck_bool_%(table_name)s_%(constraint_name)s"}`, then the output of the following:

```
op.add_column("t", "x", Boolean(name="x"))
```

will be:

```
CONSTRAINT ck_bool_t_x CHECK (x in (1, 0)))
```

The function is rendered in the output of autogenerate when a particular constraint name is already converted.

get\_bind () → Connection [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.get_bind "Link to this definition")

Return the current ‘bind’.

Under normal circumstances, this is the [`Connection`](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection "(in SQLAlchemy v2.0)") currently being used to emit SQL to the database.

In a SQL script context, this value is `None`. \[TODO: verify this\]

get\_context () → [MigrationContext](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.get_context "Link to this definition")

Return the [`MigrationContext`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext") object that’s currently in use.

*classmethod* implementation\_for (*op\_cls:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*, *replace:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") \= False*) → [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.14)") \[\[\_C\],\_C\] [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.implementation_for "Link to this definition")

Register an implementation for a given [`MigrateOperation`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.MigrateOperation "alembic.operations.ops.MigrateOperation").

Parameters:

**replace** –

when True, allows replacement of an already registered implementation for the given operation class. This enables customization of built-in operations such as [`CreateTableOp`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.CreateTableOp "alembic.operations.ops.CreateTableOp") by providing an alternate implementation that can augment, modify, or conditionally invoke the default behavior.

This is part of the operation extensibility API.

See also

[Operation Plugins](https://alembic.sqlalchemy.org/en/latest/api/operations.html#operation-plugins)

[Extending Existing Operations](https://alembic.sqlalchemy.org/en/latest/api/operations.html#operations-extending-builtin)

inline\_literal (*value:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")*, *type\_:TypeEngine \[Any\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → \_literal\_bindparam [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.inline_literal "Link to this definition")

Produce an ‘inline literal’ expression, suitable for using in an INSERT, UPDATE, or DELETE statement.

When using Alembic in “offline” mode, CRUD operations aren’t compatible with SQLAlchemy’s default behavior surrounding literal values, which is that they are converted into bound values and passed separately into the `execute()` method of the DBAPI cursor. An offline SQL script needs to have these rendered inline. While it should always be noted that inline literal values are an **enormous** security hole in an application that handles untrusted input, a schema migration is not run in this context, so literals are safe to render inline, with the caveat that advanced types like dates may not be supported directly by SQLAlchemy.

See for an example usage of.

The environment can also be configured to attempt to render “literal” values inline automatically, for those simple types that are supported by the dialect; see [`EnvironmentContext.configure.literal_binds`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.literal_binds "alembic.runtime.environment.EnvironmentContext.configure") for this more recently added feature.

Parameters:

- **value** – The value to render. Strings, integers, and simple numerics should be supported. Other types like boolean, dates, etc. may or may not be supported yet by various backends.
- **type\_** – optional - a [`sqlalchemy.types.TypeEngine`](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine "(in SQLAlchemy v2.0)") subclass stating the type of this value. In SQLAlchemy expressions, this is usually derived automatically from the Python type of the value itself, as well as based on the context in which the value is used.

See also

[`EnvironmentContext.configure.literal_binds`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.literal_binds "alembic.runtime.environment.EnvironmentContext.configure")

invoke (*operation:[MigrateOperation](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.MigrateOperation "alembic.operations.ops.MigrateOperation")*) → Any [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.invoke "Link to this definition")

Given a [`MigrateOperation`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.MigrateOperation "alembic.operations.ops.MigrateOperation"), invoke it in terms of this instance.

Register a new operation for this class.

This method is normally used to add new operations to the class, and possibly the class as well. All Alembic migration operations are implemented via this system, however the system is also available as a public API to facilitate adding custom operations.

See also

[Operation Plugins](https://alembic.sqlalchemy.org/en/latest/api/operations.html#operation-plugins)

rename\_table (*old\_table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *new\_table\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.rename_table "Link to this definition")

Emit an ALTER TABLE to rename a table.

Parameters:

- **old\_table\_name** – old name.
- **new\_table\_name** – new name.
- **schema** – Optional schema name to operate within. To control quoting of the schema outside of the default behavior, use the SQLAlchemy construct [`quoted_name`](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name "(in SQLAlchemy v2.0)").

run\_async (*async\_function:[Callable](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.14)") \[\[...\],[Awaitable](https://docs.python.org/3/library/typing.html#typing.Awaitable "(in Python v3.14)") \[\_T\]\]*, *\* args:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*, *\*\* kw\_args:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → \_T [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.Operations.run_async "Link to this definition")

Invoke the given asynchronous callable, passing an asynchronous [`AsyncConnection`](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection "(in SQLAlchemy v2.0)") as the first argument.

This method allows calling async functions from within the synchronous `upgrade()` or `downgrade()` alembic migration method.

The async connection passed to the callable shares the same transaction as the connection running in the migration context.

Any additional arg or kw\_arg passed to this function are passed to the provided async function.

Note

This method can be called only when alembic is called using an async dialect.

*class* alembic.operations.BatchOperations (*migration\_context:[MigrationContext](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext")*, *impl:BatchOperationsImpl | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations "Link to this definition")

Modifies the interface for batch mode.

This basically omits the `table_name` and `schema` parameters from associated methods, as these are a given when running under batch mode.

See also

Note that as of 0.8, most of the methods on this class are produced dynamically using the method.

Construct a new

Parameters:

**migration\_context** – a [`MigrationContext`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext "alembic.runtime.migration.MigrationContext") instance.

add\_column (*column:Column \[Any\]*, *\**, *insert\_before:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *insert\_after:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *if\_not\_exists:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.add_column "Link to this definition")

Issue an “add column” instruction using the current batch migration context.

See also

alter\_column (*column\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *nullable:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | Literal \[False\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= False*, *server\_default:Any \= False*, *new\_column\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *type\_:TypeEngine \[Any\] | Type \[TypeEngine \[Any\]\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *existing\_type:TypeEngine \[Any\] | Type \[TypeEngine \[Any\]\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *existing\_server\_default:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | Identity | Computed | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= False*, *existing\_nullable:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *existing\_comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *insert\_before:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *insert\_after:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* kw:Any*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.alter_column "Link to this definition")

Issue an “alter column” instruction using the current batch migration context.

Parameters are the same as that of , as well as the following option(s):

Parameters:

- **insert\_before** – String name of an existing column which this column should be placed before, when creating the new table.
- **insert\_after** – String name of an existing column which this column should be placed after, when creating the new table. If both and are omitted, the column is inserted after the last existing column in the table.

See also

create\_check\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *condition:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | ColumnElement \[[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")\] | TextClause*, *\*\* kw:Any*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.create_check_constraint "Link to this definition")

Issue a “create check constraint” instruction using the current batch migration context.

The batch form of this call omits the `source` and `schema` arguments from the call.

See also

create\_exclude\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\* elements:Any*, *\*\* kw:Any*) → Table | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.create_exclude_constraint "Link to this definition")

Issue a “create exclude constraint” instruction using the current batch migration context.

Note

This method is Postgresql specific, and additionally requires at least SQLAlchemy 1.0.

See also

create\_foreign\_key (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *referent\_table:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *local\_cols:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *remote\_cols:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *\**, *referent\_schema:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *onupdate:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *ondelete:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *deferrable:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *initially:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *match:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*, *\*\* dialect\_kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.create_foreign_key "Link to this definition")

Issue a “create foreign key” instruction using the current batch migration context.

The batch form of this call omits the `source` and `source_schema` arguments from the call.

e.g.:

```
with batch_alter_table("address") as batch_op:
    batch_op.create_foreign_key(
        "fk_user_address",
        "user",
        ["user_id"],
        ["id"],
    )
```

See also

create\_index (*index\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *columns:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.create_index "Link to this definition")

Issue a “create index” instruction using the current batch migration context.

See also

create\_primary\_key (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *columns:[List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.create_primary_key "Link to this definition")

Issue a “create primary key” instruction using the current batch migration context.

The batch form of this call omits the `table_name` and `schema` arguments from the call.

See also

create\_table\_comment (*comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")*, *\**, *existing\_comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.create_table_comment "Link to this definition")

Emit a COMMENT ON operation to set the comment for a table using the current batch migration context.

Parameters:

- **comment** – string value of the comment being registered against the specified table.
- **existing\_comment** – String value of a comment already registered on the specified table, used within autogenerate so that the operation is reversible, but not required for direct use.

create\_unique\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *columns:[Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")\]*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.create_unique_constraint "Link to this definition")

Issue a “create unique constraint” instruction using the current batch migration context.

The batch form of this call omits the `source` and `schema` arguments from the call.

See also

drop\_column (*column\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.drop_column "Link to this definition")

Issue a “drop column” instruction using the current batch migration context.

See also

drop\_constraint (*constraint\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *type\_:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.drop_constraint "Link to this definition")

Issue a “drop constraint” instruction using the current batch migration context.

The batch form of this call omits the `table_name` and `schema` arguments from the call.

See also

drop\_index (*index\_name:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\*\* kw:[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.drop_index "Link to this definition")

Issue a “drop index” instruction using the current batch migration context.

See also

drop\_table\_comment (*\**, *existing\_comment:[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.drop_table_comment "Link to this definition")

Issue a “drop table comment” operation to remove an existing comment set on a table using the current batch operations context.

Parameters:

**existing\_comment** – An optional string value of a comment already registered on the specified table.

execute (*sqltext:Executable | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*, *\**, *execution\_options:[dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") \[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),Any\] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") \= None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") [#](https://alembic.sqlalchemy.org/en/latest/#alembic.operations.BatchOperations.execute "Link to this definition")

Execute the given SQL using the current migration context.

See also