"""create message_analysis table

Revision ID: 947333f32c07
Revises: 2f2f0fbb07b1
Create Date: 2026-05-07

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "947333f32c07"
down_revision: Union[str, None] = "2f2f0fbb07b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "message_analysis",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("message_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("messages.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_score", sa.Numeric(), nullable=False),
        sa.Column("rule_reasons", postgresql.JSONB(), nullable=False),
        sa.Column("ml_score", sa.Numeric(), nullable=True),
        sa.Column("ml_details", postgresql.JSONB(), nullable=True),
        sa.Column("ai_score", sa.Numeric(), nullable=False),
        sa.Column("ai_explanation", sa.Text(), nullable=False),
        sa.Column("final_score", sa.Numeric(), nullable=False),
        sa.Column("model_version", sa.Text(), nullable=False),
        sa.Column("runtime_flags", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("rule_score >= 0 AND rule_score <= 1", name="ck_analysis_rule_score"),
        sa.CheckConstraint("ml_score >= 0 AND ml_score <= 1", name="ck_analysis_ml_score"),
        sa.CheckConstraint("ai_score >= 0 AND ai_score <= 1", name="ck_analysis_ai_score"),
        sa.CheckConstraint("final_score >= 0 AND final_score <= 1", name="ck_analysis_final_score"),
    )
    op.create_index("ix_analysis_message_id_created_at", "message_analysis", ["message_id", sa.text("created_at DESC")])
    op.create_index("ix_analysis_model_version", "message_analysis", ["model_version"])


def downgrade() -> None:
    op.drop_index("ix_analysis_model_version", table_name="message_analysis")
    op.drop_index("ix_analysis_message_id_created_at", table_name="message_analysis")
    op.drop_table("message_analysis")
