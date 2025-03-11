"""Initial migration

Revision ID: e76feb21d592
Revises: 
Create Date: 2025-03-11 21:43:57.345010

"""
from typing import Sequence, Union

from alembic import op
from datetime import datetime, date
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e76feb21d592'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'User',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.now, nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
    )

    op.create_table(
        'Category',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, index=True),
        sa.Column('category_name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('category_name'),
    )

    op.create_table(
        'Expense',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, index=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now, nullable=False),
        sa.Column('updated_at', sa.DateTime(), onupdate=datetime.now, nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['User.id']),
        sa.ForeignKeyConstraint(['category_id'], ['Category.id']),
        sa.PrimaryKeyConstraint('id'),
    )

def downgrade() -> None:
    """Downgrade schema."""

    # drop tables in reverse order of creation to avoid FK issues
    op.drop_table('Expense')
    op.drop_table('Category')
    op.drop_table('User')
