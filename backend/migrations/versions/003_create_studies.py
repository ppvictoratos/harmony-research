"""create studies and study_sessions tables

Revision ID: 003
Revises: 002
Create Date: 2026-10-22

"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "studies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("question", sa.Text(), nullable=True),
        sa.Column("conditions", sa.JSON(), nullable=False),
        sa.Column("session_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "study_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("study_id", sa.Integer(), nullable=False),
        sa.Column("session_number", sa.Integer(), nullable=False),
        sa.Column("condition", sa.String(100), nullable=False),
        sa.Column("planned_date", sa.Date(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("mood_before", sa.Integer(), nullable=True),
        sa.Column("mood_after", sa.Integer(), nullable=True),
        sa.Column("focus_before", sa.Integer(), nullable=True),
        sa.Column("focus_after", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["study_id"], ["studies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_study_sessions_study_id", "study_sessions", ["study_id"])


def downgrade() -> None:
    op.drop_index("ix_study_sessions_study_id", table_name="study_sessions")
    op.drop_table("study_sessions")
    op.drop_table("studies")
