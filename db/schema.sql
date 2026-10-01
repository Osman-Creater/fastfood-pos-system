CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================
-- Multi-location Fast-Food POS + Bookkeeping System
-- PostgreSQL Schema
-- =============================================================

-- Core location and user tables
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    timezone VARCHAR(80) DEFAULT 'UTC',
    is_active BOOLEAN DEFAULT TRUE,
    parent_location_id UUID REFERENCES locations(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    username VARCHAR(100) UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE user_roles (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    location_id UUID REFERENCES locations(id),
    granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, role_id, location_id)
);

-- POS and shift tables
CREATE TABLE pos_terminals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    terminal_code VARCHAR(50) NOT NULL,
    device_name VARCHAR(150),
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    ip_address VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (location_id, terminal_code)
);

CREATE TABLE cash_drawers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    terminal_id UUID REFERENCES pos_terminals(id),
    drawer_name VARCHAR(100) NOT NULL,
    opening_float NUMERIC(12,2) NOT NULL DEFAULT 0,
    current_balance NUMERIC(12,2) NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE shifts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    cashier_user_id UUID NOT NULL REFERENCES users(id),
    terminal_id UUID REFERENCES pos_terminals(id),
    cash_drawer_id UUID REFERENCES cash_drawers(id),
    opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ,
    opening_cash NUMERIC(12,2) NOT NULL DEFAULT 0,
    expected_cash NUMERIC(12,2) NOT NULL DEFAULT 0,
    counted_cash NUMERIC(12,2) NOT NULL DEFAULT 0,
    over_short NUMERIC(12,2) NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Customers and pricing
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    customer_code VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(50),
    email VARCHAR(255),
    address TEXT,
    customer_type VARCHAR(30) DEFAULT 'walk_in',
    balance_due NUMERIC(12,2) NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (location_id, customer_code)
);

-- Menu, modifiers, and recipes
CREATE TABLE menu_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    name VARCHAR(150) NOT NULL,
    parent_category_id UUID REFERENCES menu_categories(id),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE menu_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    category_id UUID REFERENCES menu_categories(id),
    sku VARCHAR(100),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    unit_price NUMERIC(12,2) NOT NULL DEFAULT 0,
    cost_price NUMERIC(12,2) NOT NULL DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    track_inventory BOOLEAN DEFAULT TRUE,
    prep_time_minutes INTEGER,
    image_url TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (location_id, sku)
);

CREATE TABLE modifier_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    minimum_select INTEGER NOT NULL DEFAULT 0,
    maximum_select INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE modifiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    modifier_group_id UUID NOT NULL REFERENCES modifier_groups(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    extra_price NUMERIC(12,2) NOT NULL DEFAULT 0,
    cost_price NUMERIC(12,2) NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE menu_item_modifiers (
    menu_item_id UUID NOT NULL REFERENCES menu_items(id) ON DELETE CASCADE,
    modifier_group_id UUID NOT NULL REFERENCES modifier_groups(id) ON DELETE CASCADE,
    is_required BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (menu_item_id, modifier_group_id)
);

CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_item_id UUID NOT NULL UNIQUE REFERENCES menu_items(id) ON DELETE CASCADE,
    version_no INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE inventory_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    unit_of_measure VARCHAR(50) NOT NULL,
    current_quantity NUMERIC(18,4) NOT NULL DEFAULT 0,
    reorder_level NUMERIC(18,4) NOT NULL DEFAULT 0,
    unit_cost NUMERIC(12,4) NOT NULL DEFAULT 0,
    last_purchase_cost NUMERIC(12,4) DEFAULT 0,
    expiry_date TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (location_id, sku)
);

CREATE TABLE recipe_ingredients (
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    inventory_item_id UUID NOT NULL REFERENCES inventory_items(id) ON DELETE RESTRICT,
    quantity NUMERIC(18,4) NOT NULL,
    unit_of_measure VARCHAR(50) NOT NULL,
    PRIMARY KEY (recipe_id, inventory_item_id)
);

CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    name VARCHAR(200) NOT NULL,
    contact_name VARCHAR(150),
    phone VARCHAR(50),
    email VARCHAR(255),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE purchase_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    supplier_id UUID NOT NULL REFERENCES suppliers(id),
    po_number VARCHAR(100) NOT NULL UNIQUE,
    order_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expected_date TIMESTAMPTZ,
    status VARCHAR(30) DEFAULT 'draft',
    subtotal NUMERIC(12,2) DEFAULT 0,
    tax_total NUMERIC(12,2) DEFAULT 0,
    total_amount NUMERIC(12,2) DEFAULT 0,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE purchase_order_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    purchase_order_id UUID NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
    inventory_item_id UUID NOT NULL REFERENCES inventory_items(id) ON DELETE RESTRICT,
    quantity NUMERIC(18,4) NOT NULL,
    unit_cost NUMERIC(12,4) NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE goods_receipts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    purchase_order_id UUID REFERENCES purchase_orders(id),
    receipt_number VARCHAR(100) NOT NULL UNIQUE,
    receipt_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    received_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE stock_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    inventory_item_id UUID NOT NULL REFERENCES inventory_items(id) ON DELETE RESTRICT,
    movement_type VARCHAR(50) NOT NULL,
    quantity NUMERIC(18,4) NOT NULL,
    unit_cost NUMERIC(12,4) DEFAULT 0,
    reference_type VARCHAR(50),
    reference_id UUID,
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (quantity != 0)
);

CREATE TABLE stock_transfers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_location_id UUID NOT NULL REFERENCES locations(id),
    to_location_id UUID NOT NULL REFERENCES locations(id),
    transfer_number VARCHAR(100) NOT NULL UNIQUE,
    transfer_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(30) DEFAULT 'pending',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (from_location_id <> to_location_id)
);

CREATE TABLE stock_transfer_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_transfer_id UUID NOT NULL REFERENCES stock_transfers(id) ON DELETE CASCADE,
    inventory_item_id UUID NOT NULL REFERENCES inventory_items(id) ON DELETE RESTRICT,
    quantity NUMERIC(18,4) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (quantity > 0)
);

CREATE TABLE stock_counts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    count_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    counted_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    status VARCHAR(30) DEFAULT 'draft',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE stock_count_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stock_count_id UUID NOT NULL REFERENCES stock_counts(id) ON DELETE CASCADE,
    inventory_item_id UUID NOT NULL REFERENCES inventory_items(id) ON DELETE RESTRICT,
    expected_quantity NUMERIC(18,4) NOT NULL DEFAULT 0,
    counted_quantity NUMERIC(18,4) NOT NULL DEFAULT 0,
    variance NUMERIC(18,4) NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Orders and payments
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    terminal_id UUID REFERENCES pos_terminals(id),
    shift_id UUID REFERENCES shifts(id),
    cashier_user_id UUID REFERENCES users(id),
    customer_id UUID REFERENCES customers(id),
    order_number VARCHAR(100) NOT NULL UNIQUE,
    order_type VARCHAR(30) NOT NULL DEFAULT 'dine_in',
    status VARCHAR(30) NOT NULL DEFAULT 'open',
    subtotal NUMERIC(12,2) NOT NULL DEFAULT 0,
    tax_total NUMERIC(12,2) NOT NULL DEFAULT 0,
    discount_total NUMERIC(12,2) NOT NULL DEFAULT 0,
    service_fee NUMERIC(12,2) NOT NULL DEFAULT 0,
    total_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    payment_status VARCHAR(30) NOT NULL DEFAULT 'unpaid',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    menu_item_id UUID NOT NULL REFERENCES menu_items(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(12,2) NOT NULL,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    tax_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    subtotal NUMERIC(12,2) NOT NULL DEFAULT 0,
    cost_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    item_status VARCHAR(30) NOT NULL DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_item_modifiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_item_id UUID NOT NULL REFERENCES order_items(id) ON DELETE CASCADE,
    modifier_id UUID NOT NULL REFERENCES modifiers(id),
    modifier_group_id UUID NOT NULL REFERENCES modifier_groups(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    extra_price NUMERIC(12,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE taxes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50),
    rate NUMERIC(8,4) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE discounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    code VARCHAR(50) NOT NULL,
    description TEXT,
    discount_type VARCHAR(30) NOT NULL DEFAULT 'percentage',
    discount_value NUMERIC(12,2) NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    valid_from TIMESTAMPTZ,
    valid_to TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    payment_method VARCHAR(30) NOT NULL,
    payment_provider VARCHAR(100),
    amount NUMERIC(12,2) NOT NULL,
    reference_no VARCHAR(200),
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    processed_at TIMESTAMPTZ,
    settled_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (amount > 0)
);

CREATE TABLE refunds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    payment_id UUID REFERENCES payments(id),
    amount NUMERIC(12,2) NOT NULL,
    reason VARCHAR(200),
    approved_by UUID REFERENCES users(id),
    status VARCHAR(30) DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (amount > 0)
);

CREATE TABLE delivery_platforms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    name VARCHAR(150) NOT NULL,
    commission_rate NUMERIC(8,4) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Accounting structures
CREATE TABLE chart_of_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    account_code VARCHAR(50) NOT NULL,
    name VARCHAR(150) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    parent_account_id UUID REFERENCES chart_of_accounts(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (location_id, account_code)
);

CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    entry_number VARCHAR(100) NOT NULL UNIQUE,
    entry_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    entry_type VARCHAR(50) NOT NULL,
    reference_type VARCHAR(50),
    reference_id UUID,
    description TEXT,
    status VARCHAR(30) DEFAULT 'posted',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE journal_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journal_entry_id UUID NOT NULL REFERENCES journal_entries(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES chart_of_accounts(id),
    debit NUMERIC(12,2) NOT NULL DEFAULT 0,
    credit NUMERIC(12,2) NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (debit >= 0 AND credit >= 0)
);

CREATE TABLE bank_deposits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    deposit_number VARCHAR(100) NOT NULL UNIQUE,
    deposit_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    amount NUMERIC(12,2) NOT NULL,
    bank_account_id UUID,
    source VARCHAR(50) DEFAULT 'cash_sales',
    status VARCHAR(30) DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Audit and operational controls
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    action VARCHAR(100) NOT NULL,
    actor_user_id UUID REFERENCES users(id),
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for frequent queries
CREATE INDEX idx_users_location_id ON users(location_id);
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
CREATE INDEX idx_pos_terminals_location_id ON pos_terminals(location_id);
CREATE INDEX idx_cash_drawers_location_id ON cash_drawers(location_id);
CREATE INDEX idx_shifts_location_id ON shifts(location_id);
CREATE INDEX idx_shifts_cashier_user_id ON shifts(cashier_user_id);
CREATE INDEX idx_menu_items_location_id ON menu_items(location_id);
CREATE INDEX idx_menu_items_category_id ON menu_items(category_id);
CREATE INDEX idx_modifiers_location_id ON modifiers(location_id);
CREATE INDEX idx_inventory_items_location_id ON inventory_items(location_id);
CREATE INDEX idx_inventory_items_sku ON inventory_items(sku);
CREATE INDEX idx_orders_location_id ON orders(location_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_journal_entries_location_id ON journal_entries(location_id);
CREATE INDEX idx_journal_lines_entry_id ON journal_lines(journal_entry_id);
CREATE INDEX idx_journal_lines_account_id ON journal_lines(account_id);
CREATE INDEX idx_chart_of_accounts_location_id ON chart_of_accounts(location_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);

-- Trigger to auto-update updated_at columns
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_locations_updated_at
BEFORE UPDATE ON locations
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_pos_terminals_updated_at
BEFORE UPDATE ON pos_terminals
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_cash_drawers_updated_at
BEFORE UPDATE ON cash_drawers
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_shifts_updated_at
BEFORE UPDATE ON shifts
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_customers_updated_at
BEFORE UPDATE ON customers
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_menu_categories_updated_at
BEFORE UPDATE ON menu_categories
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_menu_items_updated_at
BEFORE UPDATE ON menu_items
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_modifier_groups_updated_at
BEFORE UPDATE ON modifier_groups
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_modifiers_updated_at
BEFORE UPDATE ON modifiers
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_inventory_items_updated_at
BEFORE UPDATE ON inventory_items
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_suppliers_updated_at
BEFORE UPDATE ON suppliers
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_purchase_orders_updated_at
BEFORE UPDATE ON purchase_orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_orders_updated_at
BEFORE UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Seed core roles
INSERT INTO roles (id, name, description) VALUES
    (gen_random_uuid(), 'cashier', 'Handles orders, payments, and receipts'),
    (gen_random_uuid(), 'shift_supervisor', 'Approves voids, refunds, and shift close'),
    (gen_random_uuid(), 'store_manager', 'Manages staff, inventory, and location reports'),
    (gen_random_uuid(), 'inventory_officer', 'Manages stock receiving, transfers, and counts'),
    (gen_random_uuid(), 'accountant', 'Reviews journals and financial reconciliation'),
    (gen_random_uuid(), 'head_office_admin', 'Manages multi-location system settings and reporting');

-- Seed standard chart of accounts template
-- These are company-level default accounts; a location can define its own derived accounts.
INSERT INTO chart_of_accounts (id, location_id, account_code, name, account_type, parent_account_id)
VALUES
    (gen_random_uuid(), NULL, '1000', 'Cash on Hand', 'asset', NULL),
    (gen_random_uuid(), NULL, '1010', 'Bank Account', 'asset', NULL),
    (gen_random_uuid(), NULL, '1020', 'Card Payment Clearing', 'asset', NULL),
    (gen_random_uuid(), NULL, '1030', 'Delivery Platform Clearing', 'asset', NULL),
    (gen_random_uuid(), NULL, '1100', 'Inventory - Food Ingredients', 'asset', NULL),
    (gen_random_uuid(), NULL, '1110', 'Inventory - Packaging', 'asset', NULL),
    (gen_random_uuid(), NULL, '1200', 'Accounts Receivable', 'asset', NULL),
    (gen_random_uuid(), NULL, '2000', 'Sales Tax / VAT Payable', 'liability', NULL),
    (gen_random_uuid(), NULL, '2010', 'Payroll Payable', 'liability', NULL),
    (gen_random_uuid(), NULL, '2020', 'Accounts Payable', 'liability', NULL),
    (gen_random_uuid(), NULL, '2030', 'Gift Card Liability', 'liability', NULL),
    (gen_random_uuid(), NULL, '3000', 'Food Sales', 'income', NULL),
    (gen_random_uuid(), NULL, '3010', 'Beverage Sales', 'income', NULL),
    (gen_random_uuid(), NULL, '3020', 'Delivery Sales', 'income', NULL),
    (gen_random_uuid(), NULL, '3030', 'Catering Sales', 'income', NULL),
    (gen_random_uuid(), NULL, '4000', 'Cost of Goods Sold', 'expense', NULL),
    (gen_random_uuid(), NULL, '4010', 'Food Cost', 'expense', NULL),
    (gen_random_uuid(), NULL, '4020', 'Packaging Cost', 'expense', NULL),
    (gen_random_uuid(), NULL, '4030', 'Inventory Wastage', 'expense', NULL),
    (gen_random_uuid(), NULL, '5000', 'Rent', 'expense', NULL),
    (gen_random_uuid(), NULL, '5010', 'Utilities', 'expense', NULL),
    (gen_random_uuid(), NULL, '5020', 'Salaries and Wages', 'expense', NULL),
    (gen_random_uuid(), NULL, '5030', 'Merchant Processing Fees', 'expense', NULL),
    (gen_random_uuid(), NULL, '5040', 'Delivery Platform Commission', 'expense', NULL),
    (gen_random_uuid(), NULL, '5050', 'Bank Charges', 'expense', NULL),
    (gen_random_uuid(), NULL, '6000', 'Owner Capital', 'equity', NULL),
    (gen_random_uuid(), NULL, '6010', 'Retained Earnings', 'equity', NULL),
    (gen_random_uuid(), NULL, '6020', 'Owner Drawings', 'equity', NULL);

-- End of schema
