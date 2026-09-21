"""CyberShield AI release baseline.

Revision ID: b7f3c8d91a20
Revises: None

This pre-release baseline creates the schema represented by the current
SQLAlchemy models. Existing databases already stamped at b7f3c8d91a20 are
left untouched by Alembic.
"""

from alembic import op

from app.database.database import Base
from app import models  # noqa: F401

revision = "b7f3c8d91a20"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)

def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
