"""Align WebScan storage types.

Revision ID: 6712b08ceeb4
Revises: b7f3c8d91a20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "6712b08ceeb4"
down_revision: Union[str, Sequence[str], None] = "b7f3c8d91a20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Align WebScan columns with SQLAlchemy/API contract."""

    op.alter_column(
        "web_scans",
        "response_time",
        existing_type=sa.String(length=50),
        type_=sa.Float(),
        existing_nullable=True,
    )

    op.alter_column(
        "web_scans",
        "ssl_status",
        existing_type=sa.String(length=30),
        type_=sa.Text(),
        existing_nullable=True,
    )

def downgrade() -> None:
    """Restore previous WebScan column types."""

    op.alter_column(
        "web_scans",
        "ssl_status",
        existing_type=sa.Text(),
        type_=sa.String(length=30),
        existing_nullable=True,
    )

    op.alter_column(
        "web_scans",
        "response_time",
        existing_type=sa.Float(),
        type_=sa.String(length=50),
        existing_nullable=True,
    )
