"""empty message

Revision ID: 13947d7118a2
Revises: fb484a5352ce
Create Date: 2019-03-25 15:24:53.395613

"""

# revision identifiers, used by Alembic.
revision = '13947d7118a2'
down_revision = 'fb484a5352ce'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wishlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wishlist')
    # ### end Alembic commands ###