"""Add user_notification table

Revision ID: 26c94a6d068a
Revises: 35d31d1edb72
Create Date: 2018-02-04 22:10:44.786684

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '26c94a6d068a'
down_revision = '35d31d1edb72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_name'), 'notifications', ['name'], unique=False)
    op.create_index(op.f('ix_notifications_timestamp'), 'notifications', ['timestamp'], unique=False)
    op.create_table('user_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_notification_timestamp'), 'user_notification', ['timestamp'], unique=False)
    op.drop_table('notification')
    op.add_column('users', sa.Column('last_user_notification_read_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_user_notification_read_time')
    op.create_table('notification',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('timestamp', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('payload_json', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='notification_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='notification_pkey')
    )
    op.drop_index(op.f('ix_user_notification_timestamp'), table_name='user_notification')
    op.drop_table('user_notification')
    op.drop_index(op.f('ix_notifications_timestamp'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_name'), table_name='notifications')
    op.drop_table('notifications')
    # ### end Alembic commands ###
