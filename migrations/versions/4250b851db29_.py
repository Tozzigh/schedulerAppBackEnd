"""empty message

Revision ID: 4250b851db29
Revises: 7e3cf3bc8173
Create Date: 2020-07-04 15:51:49.749104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4250b851db29'
down_revision = '7e3cf3bc8173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spacetype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('space_type')
    op.add_column('brand', sa.Column('enterprise_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'brand', 'enterprise', ['enterprise_id'], ['id'])
    op.add_column('equipment', sa.Column('space_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'equipment', 'space', ['space_id'], ['id'])
    op.add_column('schedule', sa.Column('enterprise_id', sa.Integer(), nullable=False))
    op.add_column('schedule', sa.Column('space_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'schedule', 'enterprise', ['enterprise_id'], ['id'])
    op.create_foreign_key(None, 'schedule', 'space', ['space_id'], ['id'])
    op.add_column('space', sa.Column('space_type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'space', 'spacetype', ['space_type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'space', type_='foreignkey')
    op.drop_column('space', 'space_type_id')
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_column('schedule', 'space_id')
    op.drop_column('schedule', 'enterprise_id')
    op.drop_constraint(None, 'equipment', type_='foreignkey')
    op.drop_column('equipment', 'space_id')
    op.drop_constraint(None, 'brand', type_='foreignkey')
    op.drop_column('brand', 'enterprise_id')
    op.create_table('space_type',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('spacetype')
    # ### end Alembic commands ###