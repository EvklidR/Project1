"""create

Revision ID: 08a43e00ec4f
Revises: 
Create Date: 2024-05-17 14:24:20.005669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08a43e00ec4f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('IP', 'OAO', 'OOO', 'ZAO', name='typeoforganization'), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('general_amount_of_products', sa.Integer(), nullable=True),
    sa.Column('general_amount_of_products_on_stores', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groupOfProducts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('Opt', 'Rosn', name='typeofstore'), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('FIO', sa.String(), nullable=False),
    sa.Column('login', sa.String(length=320), nullable=False),
    sa.Column('isOwner', sa.Boolean(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_licvid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('predictCount', sa.Integer(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('unit', sa.Enum('metr', 'col', 'litr', 'kilo', name='unit'), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.Column('category', sa.Enum('A', 'B', 'C', name='categoryofproduct'), nullable=True),
    sa.Column('persentOfIncome', sa.Float(precision=2), nullable=True),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['type'], ['groupOfProducts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('buy',
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.Column('idWorker', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idWorker'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('displacement',
    sa.Column('idStoreToMove', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.Column('idWorker', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStoreToMove'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idWorker'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('infoAboutInventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('idInventory', sa.Integer(), nullable=False),
    sa.Column('expectedAmount', sa.Integer(), nullable=False),
    sa.Column('amountAtFact', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idInventory'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.Column('idWorker', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idWorker'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productonstore',
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idProduct', 'idStore')
    )
    op.create_table('sale',
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idCompany', sa.Integer(), nullable=False),
    sa.Column('idWorker', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idWorker'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('infoAboutBuy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idProduct', sa.Integer(), nullable=False),
    sa.Column('idBuy', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['idBuy'], ['buy.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
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
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('idStore', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['idCompany'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idProduct'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idSale'], ['sale.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idStore'], ['stores.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idWorker'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('return')
    op.drop_table('infoAboutSale')
    op.drop_table('infoAboutBuy')
    op.drop_table('sale')
    op.drop_table('productonstore')
    op.drop_table('inventory')
    op.drop_table('infoAboutInventory')
    op.drop_table('displacement')
    op.drop_table('buy')
    op.drop_table('product')
    op.drop_table('user')
    op.drop_table('stores')
    op.drop_table('groupOfProducts')
    op.drop_table('company')
    # ### end Alembic commands ###
