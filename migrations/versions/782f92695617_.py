"""empty message

Revision ID: 782f92695617
Revises: 5a80ae95e0b8
Create Date: 2021-06-16 13:46:56.380164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782f92695617'
down_revision = '5a80ae95e0b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trips', sa.Column('destination', sa.String(length=120), nullable=False))
    op.add_column('trips', sa.Column('pickup', sa.String(length=120), nullable=False))
    op.add_column('trips', sa.Column('time_started', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('trips', 'user_id', nullable=False, new_column_name='driver_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trips', 'time_started')
    op.drop_column('trips', 'pickup')
    op.drop_column('trips', 'destination')
    op.alter_column('trips', 'driver_id', nullable=False, new_column_name='user_id')
    # ### end Alembic commands ###
