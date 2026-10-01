"""Alembic script template."""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20261001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "locations",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("timezone", sa.String(length=80), nullable=False, server_default="UTC"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("parent_location_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("location_id", sa.String(length=36), nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True, unique=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("username", sa.String(length=100), nullable=True, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "menu_items",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("location_id", sa.String(length=36), nullable=False),
        sa.Column("category_id", sa.String(length=36), nullable=True),
        sa.Column("sku", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit_price", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("cost_price", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("track_inventory", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("prep_time_minutes", sa.Integer(), nullable=True),
        sa.Column("image_url", sa.String(length=255), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "inventory_items",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("location_id", sa.String(length=36), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("unit_of_measure", sa.String(length=50), nullable=False),
        sa.Column("current_quantity", sa.Numeric(precision=18, scale=4), nullable=False, server_default="0"),
        sa.Column("reorder_level", sa.Numeric(precision=18, scale=4), nullable=False, server_default="0"),
        sa.Column("unit_cost", sa.Numeric(precision=12, scale=4), nullable=False, server_default="0"),
        sa.Column("last_purchase_cost", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("expiry_date", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("location_id", sa.String(length=36), nullable=False),
        sa.Column("terminal_id", sa.String(length=36), nullable=True),
        sa.Column("shift_id", sa.String(length=36), nullable=True),
        sa.Column("cashier_user_id", sa.String(length=36), nullable=True),
        sa.Column("customer_id", sa.String(length=36), nullable=True),
        sa.Column("order_number", sa.String(length=100), nullable=False, unique=True),
        sa.Column("order_type", sa.String(length=30), nullable=False, server_default="dine_in"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="open"),
        sa.Column("subtotal", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("tax_total", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("discount_total", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("service_fee", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("total_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("payment_status", sa.String(length=30), nullable=False, server_default="unpaid"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("order_id", sa.String(length=36), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("menu_item_id", sa.String(length=36), sa.ForeignKey("menu_items.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("unit_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("discount_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("tax_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("subtotal", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("cost_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("item_status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "payments",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("order_id", sa.String(length=36), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("payment_method", sa.String(length=30), nullable=False),
        sa.Column("payment_provider", sa.String(length=100), nullable=True),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("reference_no", sa.String(length=200), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.Column("settled_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "journal_entries",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("location_id", sa.String(length=36), nullable=False),
        sa.Column("entry_number", sa.String(length=100), nullable=False, unique=True),
        sa.Column("entry_date", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("entry_type", sa.String(length=50), nullable=False),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reference_id", sa.String(length=36), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="posted"),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "journal_lines",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("journal_entry_id", sa.String(length=36), sa.ForeignKey("journal_entries.id"), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("debit", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("credit", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "stock_transactions",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("location_id", sa.String(length=36), nullable=False),
        sa.Column("inventory_item_id", sa.String(length=36), sa.ForeignKey("inventory_items.id"), nullable=False),
        sa.Column("movement_type", sa.String(length=50), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column("unit_cost", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reference_id", sa.String(length=36), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "shifts",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("location_id", sa.String(length=36), nullable=False),
        sa.Column("cashier_user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("terminal_id", sa.String(length=36), nullable=True),
        sa.Column("cash_drawer_id", sa.String(length=36), nullable=True),
        sa.Column("opened_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("opening_cash", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("expected_cash", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("counted_cash", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("over_short", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("shifts")
    op.drop_table("stock_transactions")
    op.drop_table("journal_lines")
    op.drop_table("journal_entries")
    op.drop_table("payments")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("inventory_items")
    op.drop_table("menu_items")
    op.drop_table("users")
    op.drop_table("locations")
