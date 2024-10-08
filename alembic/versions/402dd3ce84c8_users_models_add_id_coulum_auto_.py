"""users models add id coulum auto increment

Revision ID: 402dd3ce84c8
Revises: ec00da841025
Create Date: 2024-10-09 00:43:19.341241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '402dd3ce84c8'
down_revision: Union[str, None] = 'ec00da841025'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('address', sa.String(length=200), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(length=15), nullable=True))
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('users', 'phone')
    op.drop_column('users', 'address')
    # ### end Alembic commands ###
