"""empty message

Revision ID: a3374809cb93
Revises: 35273b9be8be
Create Date: 2020-06-30 16:26:01.503893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3374809cb93'
down_revision = '35273b9be8be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('slugs', sa.Column('time_ended', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('created', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created')
    op.drop_column('slugs', 'time_ended')
    # ### end Alembic commands ###