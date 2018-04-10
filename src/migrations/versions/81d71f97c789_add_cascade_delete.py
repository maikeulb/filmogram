"""add cascade delete

Revision ID: 81d71f97c789
Revises: c10d9f1e47f8
Create Date: 2018-04-07 17:30:37.783745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81d71f97c789'
down_revision = 'c10d9f1e47f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comments_post_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('likes_post_id_fkey', 'likes', type_='foreignkey')
    op.create_foreign_key(None, 'likes', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.create_foreign_key('likes_post_id_fkey', 'likes', 'posts', ['post_id'], ['id'])
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_post_id_fkey', 'comments', 'posts', ['post_id'], ['id'])
    # ### end Alembic commands ###