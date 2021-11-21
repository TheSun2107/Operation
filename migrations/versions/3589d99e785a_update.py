"""update

Revision ID: 3589d99e785a
Revises: a25e18f07542
Create Date: 2021-12-18 02:03:16.215731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3589d99e785a'
down_revision = 'a25e18f07542'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url', sa.Column('description', sa.String(length=140), nullable=True))
    op.create_index(op.f('ix_url_description'), 'url', ['description'], unique=False)
    op.create_index(op.f('ix_url_urlname'), 'url', ['urlname'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_urlname'), table_name='url')
    op.drop_index(op.f('ix_url_description'), table_name='url')
    op.drop_column('url', 'description')
    # ### end Alembic commands ###