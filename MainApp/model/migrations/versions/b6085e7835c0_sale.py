"""sale

Revision ID: b6085e7835c0
Revises: f1639ce6ec0b
Create Date: 2024-05-20 18:51:22.896354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6085e7835c0'
down_revision: Union[str, None] = 'f1639ce6ec0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.Column('idWorker', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idWorker'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('infoAboutSale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('idSale', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idSale'], ['sale.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('return',
    sa.Column('idSale', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('in_request', 'request_rejected', 'request_approved', 'done', name='statusofreturn'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.Column('idWorker', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idSale'], ['sale.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idWorker'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('buy', 'amount')
    op.drop_column('buy', 'cost')
    op.alter_column('product', 'persentOfIncome',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'persentOfIncome',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.add_column('buy', sa.Column('cost', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('buy', sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_table('return')
    op.drop_table('infoAboutSale')
    op.drop_table('sale')
    # ### end Alembic commands ###
