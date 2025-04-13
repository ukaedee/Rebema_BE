from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import create_engine

from alembic import context

import sys
import os
from dotenv import load_dotenv
import json

# 環境変数の読み込み
load_dotenv()

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# SSL証明書のパスを設定
SSL_CA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "DigiCertGlobalRootCA.crt.pem")

from models.database import Base
from models.user import User
from models.knowledge import Knowledge
from models.file import File
from models.comment import Comment
from models.knowledge_collaborator import KnowledgeCollaborator
from models.user_activity import UserActivity

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# データベースURLを環境変数から取得
db_url = os.getenv("DATABASE_URL")



config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section, {})
    
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
        connect_args={
            "ssl": {
                "ssl": True,
                "ca": SSL_CA_PATH
            }
        }
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
