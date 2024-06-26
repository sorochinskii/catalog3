"""Abstract Printer.

Revision ID: ac4b4504966b
Revises: 89a015a99910
Create Date: 2024-06-10 16:05:40.910654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac4b4504966b'
down_revision = '89a015a99910'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.Column('is_original', sa.Boolean(), nullable=True),
    sa.Column('original_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['original_id'], ['model.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendor.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('cartridge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('device', 'vendor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device', 'vendor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_table('cartridge')
    op.drop_table('model')
    # ### end Alembic commands ###