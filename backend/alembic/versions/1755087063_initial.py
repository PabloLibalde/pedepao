from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
    )
    op.create_table(
        "windows",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=80), nullable=False, unique=True),
        sa.Column("cutoff_time", sa.String(length=8), nullable=False, server_default="13:00"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.String(length=120), nullable=False, index=True),
        sa.Column("product_id", sa.Integer, nullable=False, index=True),
        sa.Column("order_date", sa.Date, nullable=False),
    )

def downgrade() -> None:
    op.drop_table("orders")
    op.drop_table("windows")
    op.drop_table("products")
