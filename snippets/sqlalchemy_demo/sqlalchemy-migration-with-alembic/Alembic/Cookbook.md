---
author: null
description: null
published: null
source: https://alembic.sqlalchemy.org/en/latest/cookbook.html
tags:
- Alembic
- SQLAlchemy-Migration
title: Cookbook — Alembic 1.17.2 documentation
---

## Cookbook

## Contents

## Cookbook

A collection of “How-Tos” highlighting popular ways to extend Alembic.

Note

This is a new section where we catalogue various “how-tos” based on user requests. It is often the case that users will request a feature only to learn it can be provided with a simple customization.

## Building an Up to Date Database from Scratch

There’s a theory of database migrations that says that the revisions in existence for a database should be able to go from an entirely blank schema to the finished product, and back again. Alembic can roll this way. Though we think it’s kind of overkill, considering that SQLAlchemy itself can emit the full CREATE statements for any given model using [`create_all()`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all "(in SQLAlchemy v2.0)"). If you check out a copy of an application, running this will give you the entire database in one shot, without the need to run through all those migration files, which are instead tailored towards applying incremental changes to an existing database.

Alembic can integrate with a [`create_all()`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all "(in SQLAlchemy v2.0)") script quite easily. After running the create operation, tell Alembic to create a new version table, and to stamp it with the most recent revision (i.e. `head`):

```
# inside of a "create the database" script, first create
# tables:
my_metadata.create_all(engine)

# then, load the Alembic configuration and generate the
# version table, "stamping" it with the most recent rev:
from alembic.config import Config
from alembic import command
alembic_cfg = Config("/path/to/yourapp/alembic.ini")
command.stamp(alembic_cfg, "head")
```

When this approach is used, the application can generate the database using normal SQLAlchemy techniques instead of iterating through hundreds of migration scripts. Now, the purpose of the migration scripts is relegated just to movement between versions on out-of-date databases, not *new* databases. You can now remove old migration files that are no longer represented on any existing environments.

To prune old migration files, simply delete the files. Then, in the earliest, still-remaining migration file, set `down_revision` to `None`:

```
# replace this:
#down_revision = '290696571ad2'

# with this:
down_revision = None
```

That file now becomes the “base” of the migration series.

## Conditional Migration Elements

This example features the basic idea of a common need, that of affecting how a migration runs based on command line switches.

The technique to use here is simple; within a migration script, inspect the [`EnvironmentContext.get_x_argument()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.get_x_argument "alembic.runtime.environment.EnvironmentContext.get_x_argument") collection for any additional, user-defined parameters. Then take action based on the presence of those arguments.

To make it such that the logic to inspect these flags is easy to use and modify, we modify our `script.py.mako` template to make this feature available in all new revision files:

```
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

from alembic import context

def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()

def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here."""
    ${upgrades if upgrades else "pass"}

def schema_downgrades():
    """schema downgrade migrations go here."""
    ${downgrades if downgrades else "pass"}

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
```

Now, when we create a new migration file, the `data_upgrades()` and `data_downgrades()` placeholders will be available, where we can add optional data migrations:

```
"""rev one

Revision ID: 3ba2b522d10d
Revises: None
Create Date: 2014-03-04 18:05:36.992867

"""

# revision identifiers, used by Alembic.
revision = '3ba2b522d10d'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Column
from sqlalchemy.sql import table, column

from alembic import context

def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()

def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here."""
    op.create_table("my_table", Column('data', String))

def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table("my_table")

def data_upgrades():
    """Add any optional data upgrade migrations here!"""

    my_table = table('my_table',
        column('data', String),
    )

    op.bulk_insert(my_table,
        [
            {'data': 'data 1'},
            {'data': 'data 2'},
            {'data': 'data 3'},
        ]
    )

def data_downgrades():
    """Add any optional data downgrade migrations here!"""

    op.execute("delete from my_table")
```

To invoke our migrations with data included, we use the `-x` flag:

```
alembic -x data=true upgrade head
```

The [`EnvironmentContext.get_x_argument()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.get_x_argument "alembic.runtime.environment.EnvironmentContext.get_x_argument") is an easy way to support new commandline options within environment and migration scripts.

## Replaceable Objects

This recipe proposes a hypothetical way of dealing with what we might call a *replaceable* schema object. A replaceable object is a schema object that needs to be created and dropped all at once. Examples of such objects include views, stored procedures, and triggers.

See also

The Replaceable Object concept has been integrated by the [Alembic Utils](https://github.com/olirice/alembic_utils) project, which provides autogenerate and migration support for PostgreSQL functions and views. See Alembic Utils at [olirice/alembic\_utils](https://github.com/olirice/alembic_utils).

Replaceable objects present a problem in that in order to make incremental changes to them, we have to refer to the whole definition at once. If we need to add a new column to a view, for example, we have to drop it entirely and recreate it fresh with the extra column added, referring to the whole structure; but to make it even tougher, if we wish to support downgrade operations in our migration scripts, we need to refer to the *previous* version of that construct fully, and we’d much rather not have to type out the whole definition in multiple places.

This recipe proposes that we may refer to the older version of a replaceable construct by directly naming the migration version in which it was created, and having a migration refer to that previous file as migrations run. We will also demonstrate how to integrate this logic within the [Operation Plugins](https://alembic.sqlalchemy.org/en/latest/api/operations.html#operation-plugins) feature introduced in Alembic 0.8. It may be very helpful to review this section first to get an overview of this API.

### The Replaceable Object Structure

We first need to devise a simple format that represents the “CREATE XYZ” / “DROP XYZ” aspect of what it is we’re building. We will work with an object that represents a textual definition; while a SQL view is an object that we can define using a [table-metadata-like system](https://github.com/sqlalchemy/sqlalchemy/wiki/UsageRecipes/Views), this is not so much the case for things like stored procedures, where we pretty much need to have a full string definition written down somewhere. We’ll use a simple value object called `ReplaceableObject` that can represent any named set of SQL text to send to a “CREATE” statement of some kind:

```
class ReplaceableObject:
    def __init__(self, name, sqltext):
        self.name = name
        self.sqltext = sqltext
```

Using this object in a migration script, assuming a Postgresql-style syntax, looks like:

```
customer_view = ReplaceableObject(
    "customer_view",
    "SELECT name, order_count FROM customer WHERE order_count > 0"
)

add_customer_sp = ReplaceableObject(
    "add_customer_sp(name varchar, order_count integer)",
    """
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;
    """
)
```

The `ReplaceableObject` class is only one very simplistic way to do this. The structure of how we represent our schema objects is not too important for the purposes of this example; we can just as well put strings inside of tuples or dictionaries, as well as that we could define any kind of series of fields and class structures we want. The only important part is that below we will illustrate how organize the code that can consume the structure we create here.

### Create Operations for the Target Objects

We’ll use the [`Operations`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations "alembic.operations.Operations") extension API to make new operations for create, drop, and replace of views and stored procedures. Using this API is also optional; we can just as well make any kind of Python function that we would invoke from our migration scripts. However, using this API gives us operations built directly into the Alembic `op.*` namespace very nicely.

The most intricate class is below. This is the base of our “replaceable” operation, which includes not just a base operation for emitting CREATE and DROP instructions on a `ReplaceableObject`, it also assumes a certain model of “reversibility” which makes use of references to other migration files in order to refer to the “previous” version of an object:

```
from alembic.operations import Operations, MigrateOperation

class ReversibleOp(MigrateOperation):
    def __init__(self, target):
        self.target = target

    @classmethod
    def invoke_for_target(cls, operations, target):
        op = cls(target)
        return operations.invoke(op)

    def reverse(self):
        raise NotImplementedError()

    @classmethod
    def _get_object_from_version(cls, operations, ident):
        version, objname = ident.split(".")

        module = operations.get_context().script.get_revision(version).module
        obj = getattr(module, objname)
        return obj

    @classmethod
    def replace(cls, operations, target, replaces=None, replace_with=None):

        if replaces:
            old_obj = cls._get_object_from_version(operations, replaces)
            drop_old = cls(old_obj).reverse()
            create_new = cls(target)
        elif replace_with:
            old_obj = cls._get_object_from_version(operations, replace_with)
            drop_old = cls(target).reverse()
            create_new = cls(old_obj)
        else:
            raise TypeError("replaces or replace_with is required")

        operations.invoke(drop_old)
        operations.invoke(create_new)
```

The workings of this class should become clear as we walk through the example. To create usable operations from this base, we will build a series of stub classes and use [`Operations.register_operation()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.register_operation "alembic.operations.Operations.register_operation") to make them part of the `op.*` namespace:

To actually run the SQL like “CREATE VIEW” and “DROP SEQUENCE”, we’ll provide implementations using [`Operations.implementation_for()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.implementation_for "alembic.operations.Operations.implementation_for") that run straight into [`Operations.execute()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.execute "alembic.operations.Operations.execute"):

```
@Operations.implementation_for(CreateViewOp)
def create_view(operations, operation):
    operations.execute("CREATE VIEW %s AS %s" % (
        operation.target.name,
        operation.target.sqltext
    ))

@Operations.implementation_for(DropViewOp)
def drop_view(operations, operation):
    operations.execute("DROP VIEW %s" % operation.target.name)

@Operations.implementation_for(CreateSPOp)
def create_sp(operations, operation):
    operations.execute(
        "CREATE FUNCTION %s %s" % (
            operation.target.name, operation.target.sqltext
        )
    )

@Operations.implementation_for(DropSPOp)
def drop_sp(operations, operation):
    operations.execute("DROP FUNCTION %s" % operation.target.name)
```

All of the above code can be present anywhere within an application’s source tree; the only requirement is that when the `env.py` script is invoked, it includes imports that ultimately call upon these classes as well as the [`Operations.register_operation()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.register_operation "alembic.operations.Operations.register_operation") and [`Operations.implementation_for()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.implementation_for "alembic.operations.Operations.implementation_for") sequences.

### Create Initial Migrations

We can now illustrate how these objects look during use. For the first step, we’ll create a new migration to create a “customer” table:

```
$ alembic revision -m "create table"
```

We build the first revision as follows:

```
"""create table

Revision ID: 3ab8b2dfb055
Revises:
Create Date: 2015-07-27 16:22:44.918507

"""

# revision identifiers, used by Alembic.
revision = '3ab8b2dfb055'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        "customer",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('order_count', sa.Integer),
    )

def downgrade():
    op.drop_table('customer')
```

For the second migration, we will create a view and a stored procedure which act upon this table:

```
$ alembic revision -m "create views/sp"
```

This migration will use the new directives:

```
"""create views/sp

Revision ID: 28af9800143f
Revises: 3ab8b2dfb055
Create Date: 2015-07-27 16:24:03.589867

"""

# revision identifiers, used by Alembic.
revision = '28af9800143f'
down_revision = '3ab8b2dfb055'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from foo import ReplaceableObject

customer_view = ReplaceableObject(
    "customer_view",
    "SELECT name, order_count FROM customer WHERE order_count > 0"
)

add_customer_sp = ReplaceableObject(
    "add_customer_sp(name varchar, order_count integer)",
    """
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;
    """
)

def upgrade():
    op.create_view(customer_view)
    op.create_sp(add_customer_sp)

def downgrade():
    op.drop_view(customer_view)
    op.drop_sp(add_customer_sp)
```

We see the use of our new `create_view()`, `create_sp()`,`drop_view()`, and `drop_sp()` directives. Running these to “head” we get the following (this includes an edited view of SQL emitted):

```
$ alembic upgrade 28af9800143
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [alembic.runtime.migration] Running upgrade  -> 3ab8b2dfb055, create table
INFO  [sqlalchemy.engine.base.Engine]
CREATE TABLE customer (
    id SERIAL NOT NULL,
    name VARCHAR,
    order_count INTEGER,
    PRIMARY KEY (id)
)

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] INSERT INTO alembic_version (version_num) VALUES ('3ab8b2dfb055')
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 3ab8b2dfb055 -> 28af9800143f, create views/sp
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count FROM customer WHERE order_count > 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='28af9800143f' WHERE alembic_version.version_num = '3ab8b2dfb055'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
```

We see that our CREATE TABLE proceeded as well as the CREATE VIEW and CREATE FUNCTION operations produced by our new directives.

### Create Revision Migrations

Finally, we can illustrate how we would “revise” these objects. Let’s consider we added a new column `email` to our `customer` table:

```
$ alembic revision -m "add email col"
```

The migration is:

```
"""add email col

Revision ID: 191a2d20b025
Revises: 28af9800143f
Create Date: 2015-07-27 16:25:59.277326

"""

# revision identifiers, used by Alembic.
revision = '191a2d20b025'
down_revision = '28af9800143f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column("customer", sa.Column("email", sa.String()))

def downgrade():
    op.drop_column("customer", "email")
```

We now need to recreate the `customer_view` view and the `add_customer_sp` function. To include downgrade capability, we will need to refer to the **previous** version of the construct; the `replace_view()` and `replace_sp()` operations we’ve created make this possible, by allowing us to refer to a specific, previous revision. the `replaces` and `replace_with` arguments accept a dot-separated string, which refers to a revision number and an object name, such as `"28af9800143f.customer_view"`. The `ReversibleOp` class makes use of the [`Operations.get_context()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.get_context "alembic.operations.Operations.get_context") method to locate the version file we refer to:

```
$ alembic revision -m "update views/sp"
```

The migration:

```
"""update views/sp

Revision ID: 199028bf9856
Revises: 191a2d20b025
Create Date: 2015-07-27 16:26:31.344504

"""

# revision identifiers, used by Alembic.
revision = '199028bf9856'
down_revision = '191a2d20b025'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from foo import ReplaceableObject

customer_view = ReplaceableObject(
    "customer_view",
    "SELECT name, order_count, email "
    "FROM customer WHERE order_count > 0"
)

add_customer_sp = ReplaceableObject(
    "add_customer_sp(name varchar, order_count integer, email varchar)",
    """
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count, email)
        VALUES (in_name, in_order_count, email);
    END;
    $$ LANGUAGE plpgsql;
    """
)

def upgrade():
    op.replace_view(customer_view, replaces="28af9800143f.customer_view")
    op.replace_sp(add_customer_sp, replaces="28af9800143f.add_customer_sp")

def downgrade():
    op.replace_view(customer_view, replace_with="28af9800143f.customer_view")
    op.replace_sp(add_customer_sp, replace_with="28af9800143f.add_customer_sp")
```

Above, instead of using `create_view()`, `create_sp()`,`drop_view()`, and `drop_sp()` methods, we now use `replace_view()` and `replace_sp()`. The replace operation we’ve built always runs a DROP *and* a CREATE. Running an upgrade to head we see:

```
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 28af9800143f -> 191a2d20b025, add email col
INFO  [sqlalchemy.engine.base.Engine] ALTER TABLE customer ADD COLUMN email VARCHAR
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='191a2d20b025' WHERE alembic_version.version_num = '28af9800143f'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 191a2d20b025 -> 199028bf9856, update views/sp
INFO  [sqlalchemy.engine.base.Engine] DROP VIEW customer_view
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count, email FROM customer WHERE order_count > 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] DROP FUNCTION add_customer_sp(name varchar, order_count integer)
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer, email varchar)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count, email)
        VALUES (in_name, in_order_count, email);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='199028bf9856' WHERE alembic_version.version_num = '191a2d20b025'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
```

After adding our new `email` column, we see that both `customer_view` and `add_customer_sp()` are dropped before the new version is created. If we downgrade back to the old version, we see the old version of these recreated again within the downgrade for this migration:

```
$ alembic downgrade 28af9800143
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running downgrade 199028bf9856 -> 191a2d20b025, update views/sp
INFO  [sqlalchemy.engine.base.Engine] DROP VIEW customer_view
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count FROM customer WHERE order_count > 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] DROP FUNCTION add_customer_sp(name varchar, order_count integer, email varchar)
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='191a2d20b025' WHERE alembic_version.version_num = '199028bf9856'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running downgrade 191a2d20b025 -> 28af9800143f, add email col
INFO  [sqlalchemy.engine.base.Engine] ALTER TABLE customer DROP COLUMN email
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='28af9800143f' WHERE alembic_version.version_num = '191a2d20b025'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
```

## Rudimental Schema-Level Multi Tenancy for PostgreSQL, MySQL, Other Databases

**Multi tenancy** refers to an application that accommodates for many clients simultaneously. Within the scope of a database migrations tool, multi-tenancy typically refers to the practice of maintaining multiple, identical databases where each database is assigned to one client.

Alembic does not currently have explicit multi-tenant support; typically, the approach must involve running Alembic multiple times against different database URLs.

One common approach to multi-tenancy, particularly on the PostgreSQL database, is to install tenants within **individual PostgreSQL schemas**; similarly when using MySQL/MariaDB, **individual MySQL/MariaDB databases** are addressed in the same way as “schemas” on PostgreSQL.

When using PostgreSQL’s schemas, a special variable `search_path` is offered that is intended to assist with targeting of different schemas. When using MySQL or MariaDB databases, a similar command is available at the SQL level called the `USE` command. This command may be used in a similar fashion as that of PostgreSQL’s `search_path` variable to achieve a similar effect.

Overall, this recipe can be used on **any database that supports runtime modification of the current “tenant” via SQL commands on a particular connection**.

Note

SQLAlchemy includes a system of directing a common set of `Table` metadata to many schemas called [schema\_translate\_map](https://docs.sqlalchemy.org/core/connections.html#translation-of-schema-names). Alembic at the time of this writing lacks adequate support for this feature. The recipe below should be considered **interim** until Alembic has more first-class support for schema-level multi-tenancy.

The recipe below can be altered for flexibility. The primary purpose of this recipe is to illustrate how to point the Alembic process towards one PostgreSQL or MySQL/MariaDB schema or another.

1. The model metadata used as the target for autogenerate must not include any schema name for tables; the schema must be non-present or set to `None`. Otherwise, Alembic autogenerate will still attempt to compare and render tables in terms of this schema:
	```
	class A(Base):
	    __tablename__ = 'a'
	    id = Column(Integer, primary_key=True)
	    data = Column(UnicodeText())
	    foo = Column(Integer)
	    __table_args__ = {
	        "schema": None
	    }
	```
2. The [`EnvironmentContext.configure.include_schemas`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_schemas "alembic.runtime.environment.EnvironmentContext.configure") flag must also be False or not included.
3. The “tenant” will be a schema name passed to Alembic using the “-x” flag. In `env.py` an approach like the following allows `-xtenant=some_schema` to be supported by making use of [`EnvironmentContext.get_x_argument()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.get_x_argument "alembic.runtime.environment.EnvironmentContext.get_x_argument"):
	```
	from sqlalchemy import text
	def run_migrations_online():
	    connectable = engine_from_config(
	        config.get_section(config.config_ini_section),
	        prefix="sqlalchemy.",
	        poolclass=pool.NullPool,
	    )
	    current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
	    with connectable.connect() as connection:
	        if connection.dialect.name == "postgresql":
	            # set search path on the connection, which ensures that
	            # PostgreSQL will emit all CREATE / ALTER / DROP statements
	            # in terms of this schema by default
	            connection.execute(text('set search_path to "%s"' % current_tenant))
	            # in SQLAlchemy v2+ the search path change needs to be committed
	            connection.commit()
	        elif connection.dialect.name in ("mysql", "mariadb"):
	            # set "USE" on the connection, which ensures that
	            # MySQL/MariaDB will emit all CREATE / ALTER / DROP statements
	            # in terms of this schema by default
	            connection.execute(text('USE %s' % current_tenant))
	        # make use of non-supported SQLAlchemy attribute to ensure
	        # the dialect reflects tables in terms of the current tenant name
	        connection.dialect.default_schema_name = current_tenant
	        context.configure(
	            connection=connection,
	            target_metadata=target_metadata,
	        )
	        with context.begin_transaction():
	            context.run_migrations()
	```
	The current tenant is set using the PostgreSQL `search_path` variable, or the MySQL/MariaDB `USE` statement, on the connection. Note above we must employ a **non-supported SQLAlchemy workaround** at the moment which is to hardcode the SQLAlchemy dialect’s default schema name to our target schema.
	It is also important to note that the above changes **remain on the connection permanently unless reversed explicitly**. If the alembic application simply exits above, there is no issue. However if the application attempts to continue using the above connection for other purposes, it may be necessary to reset these variables back to the default, which for PostgreSQL is usually the name “public” however may be different based on configuration, and for MySQL/MariaDB is typically the “database” portion of the database URL.
4. Alembic operations will now proceed in terms of whichever schema we pass on the command line. All logged SQL will show no schema, except for reflection operations which will make use of the `default_schema_name` attribute:
	```
	[]$ alembic -x tenant=some_schema revision -m "rev1" --autogenerate
	```
5. Since all schemas are to be maintained in sync, autogenerate should be run against only **one** schema, generating new Alembic migration files. Autogenerated migration operations are then run against **all** schemas.

## Don’t Generate Empty Migrations with Autogenerate

A common request is to have the `alembic revision --autogenerate` command not actually generate a revision file if no changes to the schema is detected. Using the [`EnvironmentContext.configure.process_revision_directives`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.process_revision_directives "alembic.runtime.environment.EnvironmentContext.configure") hook, this is straightforward; place a `process_revision_directives` hook in [`MigrationContext.configure()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext.configure "alembic.runtime.migration.MigrationContext.configure") which removes the single [`MigrationScript`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.MigrationScript "alembic.operations.ops.MigrationScript") directive if it is empty of any operations:

```
# for typing purposes
from collections.abc import Iterable
from alembic.environment import MigrationContext

# this typing-only import requires alembic 1.12.1 or above
from alembic.operations import MigrationScript

def run_migrations_online():

    # ...

    def process_revision_directives(
        context: MigrationContext,
        revision: str | Iterable[str | None] | Iterable[str],
        directives: list[MigrationScript],
    ):
        assert config.cmd_opts is not None
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            assert script.upgrade_ops is not None
            if script.upgrade_ops.is_empty():
                directives[:] = []

    # connectable = ...

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives
        )

        with context.begin_transaction():
            context.run_migrations()
```

## Don’t emit DROP INDEX when the table is to be dropped as well

MySQL may complain when dropping an index that is against a column that also has a foreign key constraint on it. If the table is to be dropped in any case, the DROP INDEX isn’t necessary. This recipe will process the set of autogenerate directives such that all [`DropIndexOp`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.DropIndexOp "alembic.operations.ops.DropIndexOp") directives are removed against tables that themselves are to be dropped:

```
def run_migrations_online():

    # ...

    from alembic.operations import ops

    def process_revision_directives(context, revision, directives):
        script = directives[0]

        # process both "def upgrade()", "def downgrade()"
        for directive in (script.upgrade_ops, script.downgrade_ops):

            # make a set of tables that are being dropped within
            # the migration function
            tables_dropped = set()
            for op in directive.ops:
                if isinstance(op, ops.DropTableOp):
                    tables_dropped.add((op.table_name, op.schema))

            # now rewrite the list of "ops" such that DropIndexOp
            # is removed for those tables.   Needs a recursive function.
            directive.ops = list(
                _filter_drop_indexes(directive.ops, tables_dropped)
            )

    def _filter_drop_indexes(directives, tables_dropped):
        # given a set of (tablename, schemaname) to be dropped, filter
        # out DropIndexOp from the list of directives and yield the result.

        for directive in directives:
            # ModifyTableOps is a container of ALTER TABLE types of
            # commands.  process those in place recursively.
            if isinstance(directive, ops.ModifyTableOps) and \
                    (directive.table_name, directive.schema) in tables_dropped:
                directive.ops = list(
                    _filter_drop_indexes(directive.ops, tables_dropped)
                )

                # if we emptied out the directives, then skip the
                # container altogether.
                if not directive.ops:
                    continue
            elif isinstance(directive, ops.DropIndexOp) and \
                    (directive.table_name, directive.schema) in tables_dropped:
                # we found a target DropIndexOp.   keep looping
                continue

            # otherwise if not filtered, yield out the directive
            yield directive

    # connectable = ...

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives
        )

        with context.begin_transaction():
            context.run_migrations()
```

Whereas autogenerate, when dropping two tables with a foreign key and an index, would previously generate something like:

```
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_b_aid'), table_name='b')
    op.drop_table('b')
    op.drop_table('a')
    # ### end Alembic commands ###
```

With the above rewriter, it generates as:

```
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('b')
    op.drop_table('a')
    # ### end Alembic commands ###
```

## Don’t generate any DROP TABLE directives with autogenerate

When running autogenerate against a database that has existing tables outside of the application’s autogenerated metadata, it may be desirable to prevent autogenerate from considering any of those existing tables to be dropped. This will prevent autogenerate from detecting tables removed from the local metadata as well however this is only a small caveat.

The most direct way to achieve this using the [`EnvironmentContext.configure.include_object`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object "alembic.runtime.environment.EnvironmentContext.configure") hook. There is no need to hardcode a fixed “whitelist” of table names; the hook gives enough information in the given arguments to determine if a particular table name is not part of the local `MetaData` being autogenerated, by checking first that the type of object is `"table"`, then that `reflected` is `True`, indicating this table name is from the local database connection, not the `MetaData`, and finally that `compare_to` is `None`, indicating autogenerate is not comparing this `Table` to any `Table` in the local `MetaData` collection:

```
# in env.py

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and reflected and compare_to is None:
        return False
    else:
        return True

context.configure(
    # ...
    include_object = include_object
)
```

## Apply Custom Sorting to Table Columns within CREATE TABLE

This example illustrates use of the [`Rewriter`](https://alembic.sqlalchemy.org/en/latest/api/autogenerate.html#alembic.autogenerate.rewriter.Rewriter "alembic.autogenerate.rewriter.Rewriter") object introduced at [Fine-Grained Autogenerate Generation with Rewriters](https://alembic.sqlalchemy.org/en/latest/api/autogenerate.html#autogen-rewriter). While the rewriter grants access to the individual [`ops.MigrateOperation`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.MigrateOperation "alembic.operations.ops.MigrateOperation") objects, there are sometimes some special techniques required to get around some structural limitations that are present.

One is when trying to reorganize the order of columns in a table within a [`ops.CreateTableOp`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.CreateTableOp "alembic.operations.ops.CreateTableOp") directive. This directive, when generated by autogenerate, actually holds onto the original `Table` object as the source of its information, so attempting to reorder the `ops.CreateTableOp.columns` collection will usually have no effect. Instead, a new [`ops.CreateTableOp`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.CreateTableOp "alembic.operations.ops.CreateTableOp") object may be constructed with the new ordering. However, a second issue is that the `Column` objects inside will already be associated with the `Table` that is from the model being autogenerated, meaning they can’t be reassigned directly to a new `Table`. To get around this, we can copy all the columns and constraints using methods like `Column.copy()`.

Below we use [`Rewriter`](https://alembic.sqlalchemy.org/en/latest/api/autogenerate.html#alembic.autogenerate.rewriter.Rewriter "alembic.autogenerate.rewriter.Rewriter") to create a new [`ops.CreateTableOp`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.CreateTableOp "alembic.operations.ops.CreateTableOp") directive and to copy the `Column` objects from one into another, copying each column or constraint object and applying a new sorting scheme:

```
# in env.py

from alembic.operations import ops
from alembic.autogenerate import rewriter

writer = rewriter.Rewriter()

@writer.rewrites(ops.CreateTableOp)
def order_columns(context, revision, op):

    special_names = {"id": -100, "created_at": 1001, "updated_at": 1002}

    cols_by_key = [
        (
            special_names.get(col.key, index)
            if isinstance(col, Column)
            else 2000,
            col,
        )
        for index, col in enumerate(op.columns)
    ]

    columns = [
        col for idx, col in sorted(cols_by_key, key=lambda entry: entry[0])
    ]
    return ops.CreateTableOp(
        op.table_name, columns, schema=op.schema, **op.kw)

# ...

context.configure(
    # ...
    process_revision_directives=writer
)
```

Above, when we apply the `writer` to a table such as:

```
Table(
    "my_table",
    m,
    Column("data", String(50)),
    Column("created_at", DateTime),
    Column("id", Integer, primary_key=True),
    Column("updated_at", DateTime),
    UniqueConstraint("data", name="uq_data")
)
```

This will render in the autogenerated file as:

```
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "my_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("data", name="uq_data"),
    )
    # ### end Alembic commands ###
```

## Add IF \[NOT\] EXISTS to CREATE/DROP operations

Sometimes CREATE/DROP operations take too long during a production deployment and it is preferable to apply them offline, and still keep alembic migrations aligned and/or for test environments.

Using the rewriter makes it possible:

```
from alembic.operations import ops
from alembic.autogenerate import rewriter

writer = rewriter.Rewriter()

@writer.rewrites(ops.CreateTableOp)
@writer.rewrites(ops.CreateIndexOp)
def add_if_not_exists(context, revision, op):
    op.if_not_exists = True
    return op

@writer.rewrites(ops.DropTableOp)
@writer.rewrites(ops.DropIndexOp)
def add_if_exists(context, revision, op):
    op.if_exists = True
    return op
```

Same operation is possible for ADD/DROP COLUMN on postgresql/mariadb:

```
@writer.rewrites(ops.AddColumnOp)
def add_column_if_not_exists(context, revision, op):
    op.if_not_exists = True
    return op

@writer.rewrites(ops.DropColumnOp)
def drop_column_if_not_exists(context, revision, op):
    op.if_exists = True
    return op
```

## Don’t emit CREATE TABLE statements for Views

It is sometimes convenient to create [`Table`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table "(in SQLAlchemy v2.0)") instances for views so that they can be queried using normal SQLAlchemy techniques. Unfortunately this causes Alembic to treat them as tables in need of creation and to generate spurious `create_table()` operations. This is easily fixable by flagging such Tables and using the [`include_object`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object "alembic.runtime.environment.EnvironmentContext.configure") hook to exclude them:

```
my_view = Table('my_view', metadata, autoload=True, info=dict(is_view=True))    # Flag this as a view
```

Or, if you use declarative tables:

```
class MyView(Base):
    __tablename__ = 'my_view'
    __table_args__ = {'info': {'is_view': True}} # Flag this as a view
```

Then define `include_object` as:

```
def include_object(object, name, type_, reflected, compare_to):
    """
    Exclude views from Alembic's consideration.
    """

    return not object.info.get('is_view', False)
```

Finally, in `env.py` pass your `include_object` as a keyword argument to [`EnvironmentContext.configure()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure "alembic.runtime.environment.EnvironmentContext.configure").

## Run Multiple Alembic Environments from one.ini file

Long before Alembic had the “multiple bases” feature described in [Working with Multiple Bases](https://alembic.sqlalchemy.org/en/latest/branches.html#multiple-bases), projects had a need to maintain more than one Alembic version history in a single project, where these version histories are completely independent of each other and each refer to their own alembic\_version table, either across multiple databases, schemas, or namespaces. A simple approach was added to support this, the `--name` flag on the commandline. This flag allows named sections within the `alembic.ini` file to be present (but note it does **not apply** to `pyproject.toml` configuration, where only the `[tool.alembic]` section is used).

First, one would create an alembic.ini file of this form:

Above, in the `[DEFAULT]` section we set up a default database URL. Then we create three sections corresponding to different revision lineages in our project. Each of these directories would have its own `env.py` and set of versioning files. Then when we run the `alembic` command, we simply give it the name of the configuration we want to use:

```
alembic --name schema2 revision -m "new rev for schema 2" --autogenerate
```

Above, the `alembic` command makes use of the configuration in `[schema2]`, populated with defaults from the `[DEFAULT]` section.

The above approach can be automated by creating a custom front-end to the Alembic commandline as well.

## Print Python Code to Generate Particular Database Tables

Suppose you have a database already, and want to generate some `op.create_table()` and other directives that you’d have in a migration file. How can we automate generating that code? Suppose the database schema looks like (assume MySQL):

```
CREATE TABLE IF NOT EXISTS \`users\` (
    \`id\` int(11) NOT NULL,
    KEY \`id\` (\`id\`)
);

CREATE TABLE IF NOT EXISTS \`user_properties\` (
  \`users_id\` int(11) NOT NULL,
  \`property_name\` varchar(255) NOT NULL,
  \`property_value\` mediumtext NOT NULL,
  UNIQUE KEY \`property_name_users_id\` (\`property_name\`,\`users_id\`),
  KEY \`users_id\` (\`users_id\`),
  CONSTRAINT \`user_properties_ibfk_1\` FOREIGN KEY (\`users_id\`)
  REFERENCES \`users\` (\`id\`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Using [`ops.UpgradeOps`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.UpgradeOps "alembic.operations.ops.UpgradeOps"), [`ops.CreateTableOp`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.CreateTableOp "alembic.operations.ops.CreateTableOp"), and [`ops.CreateIndexOp`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.CreateIndexOp "alembic.operations.ops.CreateIndexOp"), we create a migration file structure, using `Table` objects that we get from SQLAlchemy reflection. The structure is passed to [`autogenerate.render_python_code()`](https://alembic.sqlalchemy.org/en/latest/api/autogenerate.html#alembic.autogenerate.render_python_code "alembic.autogenerate.render_python_code") to produce the Python code for a migration file:

```
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from alembic import autogenerate
from alembic.operations import ops

e = create_engine("mysql://scott:tiger@localhost/test")

with e.connect() as conn:
    m = MetaData()
    user_table = Table('users', m, autoload_with=conn)
    user_property_table = Table('user_properties', m, autoload_with=conn)

print(autogenerate.render_python_code(
    ops.UpgradeOps(
        ops=[
            ops.CreateTableOp.from_table(table) for table in m.tables.values()
        ] + [
            ops.CreateIndexOp.from_index(idx) for table in m.tables.values()
            for idx in table.indexes
        ]
    ))
)
```

Output:

```
# ### commands auto generated by Alembic - please adjust! ###
op.create_table('users',
sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
mysql_default_charset='latin1',
mysql_engine='InnoDB'
)
op.create_table('user_properties',
sa.Column('users_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
sa.Column('property_name', mysql.VARCHAR(length=255), nullable=False),
sa.Column('property_value', mysql.MEDIUMTEXT(), nullable=False),
sa.ForeignKeyConstraint(['users_id'], ['users.id'], name='user_properties_ibfk_1', ondelete='CASCADE'),
mysql_comment='user properties',
mysql_default_charset='utf8',
mysql_engine='InnoDB'
)
op.create_index('id', 'users', ['id'], unique=False)
op.create_index('users_id', 'user_properties', ['users_id'], unique=False)
op.create_index('property_name_users_id', 'user_properties', ['property_name', 'users_id'], unique=True)
# ### end Alembic commands ###
```

## Run Alembic Operation Objects Directly (as in from autogenerate)

The [`Operations`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations "alembic.operations.Operations") object has a method known as [`Operations.invoke()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.invoke "alembic.operations.Operations.invoke") that will generically invoke a particular operation object. We can therefore use the [`autogenerate.produce_migrations()`](https://alembic.sqlalchemy.org/en/latest/api/autogenerate.html#alembic.autogenerate.produce_migrations "alembic.autogenerate.produce_migrations") function to run an autogenerate comparison, get back a [`ops.MigrationScript`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.MigrationScript "alembic.operations.ops.MigrationScript") structure representing the changes, and with a little bit of insider information we can invoke them directly.

The traversal through the [`ops.MigrationScript`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.MigrationScript "alembic.operations.ops.MigrationScript") structure is as follows:

```
use_batch = engine.name == "sqlite"

stack = [migrations.upgrade_ops]
while stack:
    elem = stack.pop(0)

    if use_batch and isinstance(elem, ModifyTableOps):
        with operations.batch_alter_table(
            elem.table_name, schema=elem.schema
        ) as batch_ops:
            for table_elem in elem.ops:
                batch_ops.invoke(table_elem)

    elif hasattr(elem, "ops"):
        stack.extend(elem.ops)
    else:
        operations.invoke(elem)
```

Above, we detect elements that have a collection of operations by looking for the `.ops` attribute. A check for [`ModifyTableOps`](https://alembic.sqlalchemy.org/en/latest/api/operations.html#alembic.operations.ops.ModifyTableOps "alembic.operations.ops.ModifyTableOps") allows us to use a batch context if we are supporting that.

A full example follows. The overall setup here is copied from the example at [`autogenerate.compare_metadata()`](https://alembic.sqlalchemy.org/en/latest/api/autogenerate.html#alembic.autogenerate.compare_metadata "alembic.autogenerate.compare_metadata"):

```
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table

from alembic.autogenerate import produce_migrations
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.operations.ops import ModifyTableOps

engine = create_engine("sqlite://", echo=True)

with engine.connect() as conn:
    conn.execute(
        """
        create table foo (
            id integer not null primary key,
            old_data varchar(50),
            x integer
        )"""
    )

    conn.execute(
        """
        create table bar (
            data varchar(50)
        )"""
    )

metadata = MetaData()
Table(
    "foo",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", Integer),
    Column("x", Integer, nullable=False),
)
Table("bat", metadata, Column("info", String(100)))

mc = MigrationContext.configure(engine.connect())

migrations = produce_migrations(mc, metadata)

operations = Operations(mc)

use_batch = engine.name == "sqlite"

stack = [migrations.upgrade_ops]
while stack:
    elem = stack.pop(0)

    if use_batch and isinstance(elem, ModifyTableOps):
        with operations.batch_alter_table(
            elem.table_name, schema=elem.schema
        ) as batch_ops:
            for table_elem in elem.ops:
                batch_ops.invoke(table_elem)

    elif hasattr(elem, "ops"):
        stack.extend(elem.ops)
    else:
        operations.invoke(elem)
```

## Test current database revision is at head(s)

Changed in version 1.17.1: This recipe is now part of the `alembic current` command using the [`command.current.check_heads`](https://alembic.sqlalchemy.org/en/latest/api/commands.html#alembic.command.current.params.check_heads "alembic.command.current") parameter, available from the command line as `--check-heads`:

```
alembic current --check-heads

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
ERROR [alembic.util.messaging] Database is not on all head revisions
FAILED: Database is not on all head revisions
```

A recipe to determine if a database schema is up to date in terms of applying Alembic migrations. May be useful for test or installation suites to determine if the target database is up to date. Makes use of the [`MigrationContext.get_current_heads()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext.get_current_heads "alembic.runtime.migration.MigrationContext.get_current_heads") as well as [`ScriptDirectory.get_heads()`](https://alembic.sqlalchemy.org/en/latest/api/script.html#alembic.script.ScriptDirectory.get_heads "alembic.script.ScriptDirectory.get_heads") methods so that it accommodates for a branched revision tree:

```
from alembic import config, script
from alembic.runtime import migration
from sqlalchemy import engine

def check_current_head(alembic_cfg, connectable):
    # type: (config.Config, engine.Engine) -> bool
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())

e = engine.create_engine("mysql://scott:tiger@localhost/test", echo=True)
cfg = config.Config("alembic.ini")
print(check_current_head(cfg, e))
```

See also

[`MigrationContext.get_current_heads()`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.migration.MigrationContext.get_current_heads "alembic.runtime.migration.MigrationContext.get_current_heads")

[`ScriptDirectory.get_heads()`](https://alembic.sqlalchemy.org/en/latest/api/script.html#alembic.script.ScriptDirectory.get_heads "alembic.script.ScriptDirectory.get_heads")

## Using Asyncio with Alembic

SQLAlchemy version 1.4 introduced experimental support for asyncio, allowing use of most of its interface from async applications. Alembic currently does not provide an async api directly, but it can use an use SQLAlchemy Async engine to run the migrations and autogenerate.

New configurations can use the template “async” or “pyproject\_async” to bootstrap an environment which can be used with async DBAPI like asyncpg, running the command:

```
alembic init -t async <script_directory_here>
```

Existing configurations can be updated to use an async DBAPI by updating the `env.py` file that’s used by Alembic to start its operations. In particular only `run_migrations_online` will need to be updated to be something like the example below:

```
import asyncio

from sqlalchemy.ext.asyncio import async_engine_from_config

# ... no change required to the rest of the code

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online():
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())
```

An async application can also interact with the Alembic api directly by using the SQLAlchemy `run_sync` method to adapt the non-async api of Alembic to an async consumer.

### Programmatic API use (connection sharing) With Asyncio

Combining the examples of with together, the `env.py` listed above can be updated as follows works:

```
def run_migrations_online():
    """Run migrations in 'online' mode.

    """

    connectable = config.attributes.get("connection", None)

    if connectable is None:
        asyncio.run(run_async_migrations())
    else:
        do_run_migrations(connectable)
```

Above, using an asyncio database URL in `alembic.ini` one can run commands such as `alembic upgrade` from the command line. Programmatically, the same `env.py` file can be invoked using asyncio as:

```
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import command, config

def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")

async def run_async_upgrade():
    async_engine = create_async_engine("sqlite+aiosqlite://", echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, config.Config("alembic.ini"))

asyncio.run(run_async_upgrade())
```

## Data Migrations - General Techniques

Alembic migrations are designed for schema migrations. The nature of data migrations are inherently different and it’s not in fact advisable in the general case to write data migrations that integrate with Alembic’s schema versioning model. For example downgrades are difficult to address since they might require deletion of data, which may even not be possible to detect.

Warning

The solution needs to be designed specifically for each individual application and migration. There are no general rules and the following text is only a recommendation based on experience.

There are three basic approaches for the data migrations.

### Small data

Small data migrations are easy to perform, especially in cases of initial data to a new table. These can be handled using [`Operations.bulk_insert()`](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.bulk_insert "alembic.operations.Operations.bulk_insert").

### Separate migration script

One possibility is a completely separate script aside of alembic migrations. The complete migration is then processed in following steps:

1. Run the initial alembic migrations (new columns etc.)
2. Run the separate data migration script
3. Run the final alembic migrations (database constraints, delete columns etc.)

The data migration script may also need a separate ORM model to handle intermediate state of the database.

### Online migration

The application maintains a version of schema with both versions. Writes are performed on both places, while the background script move all the remaining data across. This technique is very challenging and time demanding, since it requires custom application logic to handle the intermediate states.

## Extend CommandLine with custom commands

While Alembic does not have a plugin system that would allow transparently extending the original `alembic` CLI with additional commands, it is possible to create your own instance of [`CommandLine`](https://alembic.sqlalchemy.org/en/latest/api/config.html#alembic.config.CommandLine "alembic.config.CommandLine") and extend that via [`CommandLine.register_command()`](https://alembic.sqlalchemy.org/en/latest/api/config.html#alembic.config.CommandLine.register_command "alembic.config.CommandLine.register_command").

Any named function may be registered as a command, provided it accepts a [`Config`](https://alembic.sqlalchemy.org/en/latest/api/config.html#alembic.config.Config "alembic.config.Config") object as the first argument; a docstring is also recommended as it will show up in the help output of the CLI.

```
$ python -m myalembic -h
...
positional arguments:
  {branches,check,current,downgrade,edit,ensure_version,heads,history,init,list_templates,merge,revision,show,stamp,upgrade,frobnicate}
    ...
    frobnicate          Frobnicates according to the frobnication specification.

$ python -m myalembic frobnicate -h
usage: myalembic.py frobnicate [-h] revision

positional arguments:
revision    revision identifier

optional arguments:
-h, --help  show this help message and exit

$ python -m myalembic frobnicate 42
Revision 42 successfully frobnicated.
```