"""Add interview proctoring events table

Revision ID: a1b2c3d4e5f6
Revises: e172df5dba7e
Create Date: 2026-08-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'e172df5dba7e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'interview_proctor_events',
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('interview_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['interview_id'], ['interviews.interview_id'], ),
        sa.PrimaryKeyConstraint('event_id')
    )


def downgrade():
    op.drop_table('interview_proctor_events')
