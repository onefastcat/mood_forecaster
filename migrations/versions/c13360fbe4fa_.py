"""empty message

Revision ID: c13360fbe4fa
Revises: ae45703f9e1e
Create Date: 2023-01-22 14:47:59.008974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c13360fbe4fa'
down_revision = 'ae45703f9e1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_point',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('mood_value', sa.INTEGER(), nullable=False),
    sa.Column('energy_value', sa.INTEGER(), nullable=False),
    sa.Column('temperature', sa.FLOAT(), nullable=False),
    sa.Column('pressure', sa.FLOAT(), nullable=False),
    sa.Column('precipitation', sa.FLOAT(), nullable=False),
    sa.Column('date_created', sa.DATE(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_point')
    # ### end Alembic commands ###
