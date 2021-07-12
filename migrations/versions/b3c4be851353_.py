"""empty message

Revision ID: b3c4be851353
Revises: 346eafd3764f
Create Date: 2021-07-12 17:17:55.155017

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b3c4be851353'
down_revision = '346eafd3764f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trip_history',
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('time_started', sa.DateTime(timezone=True), nullable=True),
    sa.Column('time_ended', sa.DateTime(timezone=True), nullable=True),
    sa.Column('pickup', sa.String(length=120), nullable=False),
    sa.Column('destination', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('trips', 'time_ended')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trips', sa.Column('time_ended', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_table('trip_history')
    # ### end Alembic commands ###