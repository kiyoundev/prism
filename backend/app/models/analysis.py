import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class MessageAnalysis(Base):
    __tablename__ = "message_analysis"

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    )
    message_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
    )
    rule_score = sa.Column(
        sa.Numeric,
        sa.CheckConstraint(
            "rule_score >= 0 AND rule_score <= 1", name="ck_analysis_rule_score"
        ),
        nullable=False,
    )
    rule_reasons = sa.Column(JSONB, nullable=False)
    ml_score = sa.Column(
        sa.Numeric,
        sa.CheckConstraint(
            "ml_score >= 0 AND ml_score <= 1", name="ck_analysis_ml_score"
        ),
        nullable=True,
    )
    ml_details = sa.Column(JSONB, nullable=True)
    ai_score = sa.Column(
        sa.Numeric,
        sa.CheckConstraint(
            "ai_score >= 0 AND ai_score <= 1", name="ck_analysis_ai_score"
        ),
        nullable=False,
    )
    ai_explanation = sa.Column(sa.Text, nullable=False)
    final_score = sa.Column(
        sa.Numeric,
        sa.CheckConstraint(
            "final_score >= 0 AND final_score <= 1", name="ck_analysis_final_score"
        ),
        nullable=False,
    )
    model_version = sa.Column(sa.Text, nullable=False)
    runtime_flags = sa.Column(JSONB, nullable=False)
    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")
    )

    message = relationship("Message", back_populates="analyses")

    __table_args__ = (
        sa.Index(
            "ix_analysis_message_id_created_at",
            "message_id",
            sa.text("created_at DESC"),
        ),
        sa.Index("ix_analysis_model_version", "model_version"),
    )
