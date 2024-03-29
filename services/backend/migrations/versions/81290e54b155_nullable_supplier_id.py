"""nullable supplier_id

Revision ID: 81290e54b155
Revises: 6db44337c4bf
Create Date: 2024-02-06 06:00:26.089264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81290e54b155'
down_revision: Union[str, None] = '6db44337c4bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parts', 'supplier_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parts', 'supplier_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
