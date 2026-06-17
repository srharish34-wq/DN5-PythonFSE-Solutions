# ============================================================
# Module 3 – Hands On 7: Alembic Migration Setup — env.py
# Cognizant DN5.0 | Harish Seetharaman Rama
#
# SETUP STEPS (run once in terminal):
#   cd orm/
#   alembic init migrations
#   Then REPLACE migrations/env.py with this file
#
# alembic.ini — change this line:
#   sqlalchemy.url = mysql+mysqlconnector://root:password@localhost/college_db_orm
#
# COMMANDS:
#   alembic revision --autogenerate -m "initial schema"     → create migration 1
#   alembic upgrade head                                    → apply all migrations
#   alembic revision --autogenerate -m "add is_active"     → create migration 2
#   alembic revision --autogenerate -m "add course_schedule"→ create migration 3
#   alembic history --verbose                               → see all revisions
#   alembic current                                         → see current version
#   alembic downgrade -1                                    → rollback 1 step
#   alembic downgrade base                                  → rollback everything
# ============================================================

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys, os

# Make models importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This tells Alembic about your models so --autogenerate works
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# ============================================================
# MIGRATION HISTORY THIS PROJECT WILL HAVE:
#
# Rev 1: "initial schema"
#   upgrade()   → creates departments, students, courses,
#                 enrollments, professors tables
#   downgrade() → drops all tables
#
# Rev 2: "add is_active to students"
#   upgrade()   → op.add_column('students', Column('is_active', Boolean, default=True))
#   downgrade() → op.drop_column('students', 'is_active')
#
# Rev 3: "add course_schedules table"
#   upgrade()   → op.create_table('course_schedules', ...)
#   downgrade() → op.drop_table('course_schedules')
#
# After alembic upgrade head:
#   alembic history shows 3 revisions
#   alembic downgrade -1 → drops course_schedules
#   alembic upgrade head → recreates course_schedules
# ============================================================
