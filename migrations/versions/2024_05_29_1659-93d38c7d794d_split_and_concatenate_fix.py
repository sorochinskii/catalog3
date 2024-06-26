"""split_and_concatenate fix.

Revision ID: 93d38c7d794d
Revises: aa8151204913
Create Date: 2024-05-29 16:59:51.599266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d38c7d794d'
down_revision = 'aa8151204913'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mfp_network',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mac', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['device.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('m_f_p_network')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('m_f_p_network',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('mac', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['device.id'], name='m_f_p_network_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='m_f_p_network_pkey')
    )
    op.drop_table('mfp_network')
    # ### end Alembic commands ###
