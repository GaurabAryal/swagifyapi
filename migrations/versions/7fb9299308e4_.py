"""empty message

Revision ID: 7fb9299308e4
Revises: 73433710d40c
Create Date: 2019-03-24 19:12:09.659822

"""

# revision identifiers, used by Alembic.
revision = '7fb9299308e4'
down_revision = '73433710d40c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(length=100), nullable=True))
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('users', 'name')
    # ### end Alembic commands ###
