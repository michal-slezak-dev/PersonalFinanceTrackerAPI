"""Add first_name and last_name to User model

Revision ID: ab602816b6fb
Revises: e76feb21d592
Create Date: 2025-03-11 22:47:42.683256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ab602816b6fb'
down_revision: Union[str, None] = 'e76feb21d592'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('User', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('User', sa.Column('last_name', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('User', 'firstname')
    op.drop_column('User', 'lastname')
