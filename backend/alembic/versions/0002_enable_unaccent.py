from alembic import op

revision = "0002_enable_unaccent"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent")


def downgrade():
    # Em geral não removemos extensão em downgrade, mas se quiser:
    # op.execute("DROP EXTENSION IF EXISTS unaccent")
    pass
