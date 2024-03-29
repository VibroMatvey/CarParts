"""Sales and SalesStatuses

Revision ID: eb581707ba68
Revises: 257aee67e729
Create Date: 2024-02-12 23:24:18.024710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb581707ba68'
down_revision: Union[str, None] = '257aee67e729'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sales_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sales_statuses_id'), 'sales_statuses', ['id'], unique=False)
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('part_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['part_id'], ['parts.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['sales_statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sales_id'), 'sales', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sales_id'), table_name='sales')
    op.drop_table('sales')
    op.drop_index(op.f('ix_sales_statuses_id'), table_name='sales_statuses')
    op.drop_table('sales_statuses')
    # ### end Alembic commands ###
