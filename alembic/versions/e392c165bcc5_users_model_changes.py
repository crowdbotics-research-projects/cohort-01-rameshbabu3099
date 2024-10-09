""" users model changes

Revision ID: e392c165bcc5
Revises: 1871c94d64eb
Create Date: 2024-10-09 00:26:50.697007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e392c165bcc5'
down_revision: Union[str, None] = '1871c94d64eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
