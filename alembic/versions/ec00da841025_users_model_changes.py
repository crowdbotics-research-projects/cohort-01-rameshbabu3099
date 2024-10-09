""" users model changes

Revision ID: ec00da841025
Revises: e392c165bcc5
Create Date: 2024-10-09 00:39:10.715158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec00da841025'
down_revision: Union[str, None] = 'e392c165bcc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
