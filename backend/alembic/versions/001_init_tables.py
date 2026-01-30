from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("telegram_id", sa.BigInteger, unique=True, nullable=False),
        sa.Column("consent_given", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "poi",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.String),
    )

    op.create_table(
        "media",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("poi_id", sa.Integer, sa.ForeignKey("poi.id")),
        sa.Column("url", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("media")
    op.drop_table("poi")
    op.drop_table("users")
