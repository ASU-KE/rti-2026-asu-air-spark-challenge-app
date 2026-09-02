# Alembic & SQLAlchemy Migration Reference

Workflow, wiring, and gotchas for the migration tool referenced by [`SKILL.md`](SKILL.md): Alembic, the migration tool for SQLAlchemy and the standard choice for a FastAPI backend on PostgreSQL. The safety rules, PostgreSQL patterns, and expand-contract strategy in `SKILL.md` apply on top of this workflow.

## Autogenerate Workflow

Alembic compares your SQLAlchemy models against the live database and drafts a migration for the diff.

```bash
# Draft a migration from model changes (compares metadata to the database)
alembic revision --autogenerate -m "add user avatar"

# Review and edit the generated script under versions/ BEFORE applying it

# Apply all pending migrations up to the latest revision
alembic upgrade head

# Roll back the most recent migration
alembic downgrade -1

# Inspect state
alembic current   # revision the database is on
alembic history   # full revision graph
```

The generated script lands in `versions/<revision>_add_user_avatar.py` with `upgrade()` and `downgrade()` functions built from `op` directives.

## Wiring env.py to Model Metadata

Autogenerate only works when `target_metadata` points at the `MetaData` your models are registered on. In `alembic/env.py`:

```python
# Import the Base your models inherit from, so its metadata is populated
from app.db.base import Base  # Base = declarative_base()
import app.models  # noqa: F401 — ensures every model is imported and registered

target_metadata = Base.metadata
```

If a model module is never imported before `env.py` reads `Base.metadata`, its table is invisible to autogenerate — import the package that pulls in all models.

## Autogenerate Does Not Detect Every Change

Autogenerate is a starting point, not a source of truth. Always read the generated script and edit it before applying. It reliably detects added/removed tables and columns, index and unique-constraint changes, and most type changes, but it misses or misreads:

- **Server defaults** — changes to `server_default` are not detected unless `compare_server_default=True` is set in `context.configure(...)`, and even then detection is best-effort.
- **Column and table renames** — a rename is emitted as a `drop_column` + `add_column` (or drop/create table), which destroys data. Rewrite it by hand as `op.alter_column(..., new_column_name=...)` or `op.rename_table(...)`.
- **Enum / custom type changes** — adding a value to a PostgreSQL `ENUM`, or altering a type, is not generated; write the `ALTER TYPE ... ADD VALUE` (or a create/swap) manually.
- **`CHECK` constraints and other unnamed constraints** — often skipped; add them explicitly.

Because of this, the review step is mandatory, not optional.

## Concurrent Index (Outside the Transaction)

Alembic wraps each migration in a transaction, but `CREATE INDEX CONCURRENTLY` cannot run inside one. Use an autocommit block so the index build runs on its own connection:

```python
def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.create_index(
            "idx_users_email",
            "users",
            ["email"],
            postgresql_concurrently=True,
            if_not_exists=True,
        )

def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.drop_index("idx_users_email", "users", postgresql_concurrently=True)
```

## Data Migration

Keep DML in its own revision, separate from schema DDL (see the safety checklist in `SKILL.md`). Use batched updates for large tables rather than one table-wide statement:

```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    conn = op.get_bind()
    while True:
        result = conn.execute(
            sa.text(
                """
                UPDATE users SET display_name = username
                WHERE id IN (
                    SELECT id FROM users
                    WHERE display_name IS NULL
                    LIMIT 5000
                    FOR UPDATE SKIP LOCKED
                )
                """
            )
        )
        if result.rowcount == 0:
            break

def downgrade() -> None:
    pass  # data backfill has no meaningful reverse
```
