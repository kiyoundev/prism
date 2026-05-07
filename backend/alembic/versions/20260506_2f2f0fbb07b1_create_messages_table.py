"""create messages table

Revision ID: 2f2f0fbb07b1
Revises:
Create Date: 2026-05-06

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "2f2f0fbb07b1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column("category", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.CheckConstraint("source IN ('seed_scam', 'seed_legit', 'user_submitted')", name="ck_messages_source"),
        sa.CheckConstraint("label IN ('scam', 'legit', 'unknown')", name="ck_messages_label"),
    )
    op.create_index("ix_messages_source", "messages", ["source"])
    op.create_index("ix_messages_label", "messages", ["label"])
    op.create_index("ix_messages_created_at_desc", "messages", [sa.text("created_at DESC")])


def downgrade() -> None:
    op.drop_index("ix_messages_created_at_desc", table_name="messages")
    op.drop_index("ix_messages_label", table_name="messages")
    op.drop_index("ix_messages_source", table_name="messages")
    op.drop_table("messages")
