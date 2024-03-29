"""empty message

Revision ID: 4a6c317ffaac
Revises: e069891b07c5
Create Date: 2021-06-18 14:39:25.032196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a6c317ffaac'
down_revision = 'e069891b07c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trips', sa.Column('qr_string', sa.String(length=18), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trips', 'qr_string')
    # ### end Alembic commands ###
