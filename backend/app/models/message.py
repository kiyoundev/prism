import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    )
    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")
    )
    text = sa.Column(sa.Text, nullable=False)
    source = sa.Column(
        sa.Text,
        sa.CheckConstraint(
            "source IN ('seed_scam', 'seed_legit', 'user_submitted')",
            name="ck_messages_source",
        ),
        nullable=False,
    )
    label = sa.Column(
        sa.Text,
        sa.CheckConstraint(
            "label IN ('scam', 'legit', 'unknown')",
            name="ck_messages_label",
        ),
        nullable=False,
    )
    category = sa.Column(sa.Text, nullable=True)
    metadata_ = sa.Column("metadata", JSONB, nullable=True)

    analyses = relationship(
        "MessageAnalysis", back_populates="message", cascade="all, delete-orphan"
    )

    __table_args__ = (
        sa.Index("ix_messages_source", "source"),
        sa.Index("ix_messages_label", "label"),
        sa.Index("ix_messages_created_at_desc", sa.text("created_at DESC")),
    )
