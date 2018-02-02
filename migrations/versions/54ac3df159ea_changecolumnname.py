"""ChangeColumnName

Revision ID: 54ac3df159ea
Revises: 9ff9965d6d5e
Create Date: 2018-02-01 19:59:14.989680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54ac3df159ea'
down_revision = '9ff9965d6d5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('photo_filename', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('photo_url', sa.String(), nullable=True))
    op.drop_constraint('posts_user_id_fkey', 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('posts_user_id_fkey', 'posts', 'users', ['user_id'], ['id'])
    op.drop_column('posts', 'photo_url')
    op.drop_column('posts', 'photo_filename')
    # ### end Alembic commands ###
