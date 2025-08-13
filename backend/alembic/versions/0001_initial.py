from alembic import op
import sqlalchemy as sa

# Revisões
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # products
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
    )
    op.create_index("ix_products_name", "products", ["name"], unique=False)

    # offers
    op.create_table(
        "offers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("product_id", sa.Integer, nullable=False),
        sa.Column("cutoff_time", sa.String(length=8), nullable=False, server_default="13:00"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
    )
    op.create_index("ix_offers_product_id", "offers", ["product_id"], unique=False)
    op.create_foreign_key(
        "fk_offers_product_id_products",
        "offers",
        "products",
        ["product_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # orders
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.String(length=120), nullable=False),
        sa.Column("product_id", sa.Integer, nullable=False),
        sa.Column("order_date", sa.Date, nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name="fk_orders_product_id_products",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("user_id", "order_date", name="uq_order_user_day"),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"], unique=False)
    op.create_index("ix_orders_product_id", "orders", ["product_id"], unique=False)
    op.create_index("ix_orders_order_date", "orders", ["order_date"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_orders_order_date", table_name="orders")
    op.drop_index("ix_orders_product_id", table_name="orders")
    op.drop_index("ix_orders_user_id", table_name="orders")
    op.drop_table("orders")

    op.drop_constraint("fk_offers_product_id_products", "offers", type_="foreignkey")
    op.drop_index("ix_offers_product_id", table_name="offers")
    op.drop_table("offers")

    op.drop_index("ix_products_name", table_name="products")
    op.drop_table("products")
