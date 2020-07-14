"""empty message

Revision ID: 4bd41ad64899
Revises: a3374809cb93
Create Date: 2020-07-01 21:08:50.654558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bd41ad64899'
down_revision = 'a3374809cb93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('slugs', sa.Column('created_timestamp', sa.DateTime(), nullable=True))
    op.add_column('slugs', sa.Column('slug_id', sa.Integer(), nullable=False))
    op.add_column('slugs', sa.Column('time_ended', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('slugs', 'carpool_id')
    op.add_column('users', sa.Column('created_timestamp', sa.DateTime(), nullable=True))
    op.alter_column('users', 'phone_number',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('users', 'created_timestamp')
    op.add_column('slugs', sa.Column('carpool_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('slugs', 'time_ended')
    op.drop_column('slugs', 'slug_id')
    op.drop_column('slugs', 'created_timestamp')
    # ### end Alembic commands ###