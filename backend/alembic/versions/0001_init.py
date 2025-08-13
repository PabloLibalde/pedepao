from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('offers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    op.create_table('offer_windows',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('offer_id', sa.Integer(), sa.ForeignKey('offers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('weekdays', sa.String(length=50), nullable=False, server_default='1,2,3,4,5'),
        sa.Column('cutoff_local_time', sa.String(length=5), nullable=False, server_default='13:00')
    )

    op.create_table('orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('offer_id', sa.Integer(), sa.ForeignKey('offers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('order_date', sa.Date(), nullable=False),
        sa.Column('chosen_at_utc', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_unique_constraint('uq_user_orderdate', 'orders', ['user_id', 'order_date'])

def downgrade():
    op.drop_constraint('uq_user_orderdate', 'orders', type_='unique')
    op.drop_table('orders')
    op.drop_table('offer_windows')
    op.drop_table('offers')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
