from alembic import op

revision = "0002_unique_order_user_day"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_unique_constraint("uq_order_user_day", "orders", ["user_id", "order_date"])

def downgrade() -> None:
    op.drop_constraint("uq_order_user_day", "orders", type_="unique")
