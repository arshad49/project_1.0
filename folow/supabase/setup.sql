-- Customers table
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    last_visit DATE,
    next_followup DATE,
    template_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_customers_next_followup ON customers(next_followup);
CREATE INDEX idx_customers_status ON customers(status);
CREATE INDEX idx_customers_phone ON customers(phone);

-- Valid template_name values:
-- "follow_up_basic"
-- "festival_offer"
-- "discount_offer"
