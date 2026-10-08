"""Merge scheduled datetime with existing head

Revision ID: d87764fd8585
Revises: 8e21c8272e9f, add_scheduled_datetime
Create Date: 2026-08-04 10:51:17.890954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd87764fd8585'
down_revision = ('8e21c8272e9f', 'add_scheduled_datetime')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
