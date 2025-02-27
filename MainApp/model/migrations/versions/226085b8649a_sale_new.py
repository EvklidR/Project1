"""sale new

Revision ID: 226085b8649a
Revises: b6085e7835c0
Create Date: 2024-05-20 20:48:57.164065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '226085b8649a'
down_revision: Union[str, None] = 'b6085e7835c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('buy_idProduct_fkey', 'buy', type_='foreignkey')
    op.drop_column('buy', 'idProduct')
    op.drop_constraint('inventory_idProduct_fkey', 'inventory', type_='foreignkey')
    op.drop_column('inventory', 'idProduct')
    op.alter_column('product', 'persentOfIncome',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    op.drop_constraint('sale_idProduct_fkey', 'sale', type_='foreignkey')
    op.drop_column('sale', 'idProduct')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sale', sa.Column('idProduct', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('sale_idProduct_fkey', 'sale', 'product', ['idProduct'], ['id'], ondelete='CASCADE')
    op.alter_column('product', 'persentOfIncome',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.add_column('inventory', sa.Column('idProduct', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('inventory_idProduct_fkey', 'inventory', 'product', ['idProduct'], ['id'], ondelete='CASCADE')
    op.add_column('buy', sa.Column('idProduct', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('buy_idProduct_fkey', 'buy', 'product', ['idProduct'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
