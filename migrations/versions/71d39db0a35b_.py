"""empty message

Revision ID: 71d39db0a35b
Revises: b3c4be851353
Create Date: 2021-07-12 17:26:08.189476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71d39db0a35b'
down_revision = 'b3c4be851353'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passenger_history',
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['trip_id'], ['trip_history.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('passenger_history')
    # ### end Alembic commands ###