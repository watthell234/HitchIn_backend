"""empty message

Revision ID: 3586505f3366
Revises: bd8f27ec0410
Create Date: 2020-07-13 23:58:52.185324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3586505f3366'
down_revision = 'bd8f27ec0410'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('owner_id', sa.String(length=18), nullable=False))
    op.create_foreign_key(None, 'cars', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cars', type_='foreignkey')
    op.drop_column('cars', 'owner_id')
    # ### end Alembic commands ###