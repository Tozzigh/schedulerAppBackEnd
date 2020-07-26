"""empty message

Revision ID: fa8e47c423ff
Revises: 907df834e013
Create Date: 2020-07-26 09:07:09.417928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa8e47c423ff'
down_revision = '907df834e013'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enterprise', sa.Column('tot_hours', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('enterprise', 'tot_hours')
    # ### end Alembic commands ###