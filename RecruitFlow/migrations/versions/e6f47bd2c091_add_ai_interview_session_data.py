"""Store AI interview outcomes and recordings

Revision ID: e6f47bd2c091
Revises: d87764fd8585
Create Date: 2026-09-28

"""
from alembic import op
import sqlalchemy as sa


revision = "e6f47bd2c091"
down_revision = "d87764fd8585"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("interviews") as batch_op:
        batch_op.add_column(sa.Column("ai_final_score", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("ai_transcript", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("ai_recording_path", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("ai_duration_seconds", sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table("interviews") as batch_op:
        batch_op.drop_column("ai_duration_seconds")
        batch_op.drop_column("ai_recording_path")
        batch_op.drop_column("ai_transcript")
        batch_op.drop_column("ai_final_score")