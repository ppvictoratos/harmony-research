"""create evidence table

Revision ID: 001
Revises:
Create Date: 2026-10-21

"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "evidence",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("study_id", sa.String(50), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("authors", sa.Text(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("intervention_type", sa.String(100), nullable=True),
        sa.Column("intervention_details", sa.Text(), nullable=True),
        sa.Column("outcomes", sa.Text(), nullable=True),
        sa.Column("sample_size", sa.Integer(), nullable=True),
        sa.Column("effect_size", sa.Float(), nullable=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("url", sa.String(500), nullable=True),
        sa.Column("date_added", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("study_id", name="uq_evidence_study_id"),
    )
    op.create_index("ix_evidence_source_year", "evidence", ["source", "year"])
    op.create_index("ix_evidence_intervention", "evidence", ["intervention_type"])


def downgrade() -> None:
    op.drop_index("ix_evidence_intervention", table_name="evidence")
    op.drop_index("ix_evidence_source_year", table_name="evidence")
    op.drop_table("evidence")
