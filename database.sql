-- ============================
-- URL SHORTENER DATABASE
-- ============================

-- Create users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create urls table
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(20) NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
);

-- Create clicks table
CREATE TABLE clicks (
    id BIGSERIAL PRIMARY KEY,
    url_id BIGINT NOT NULL,
    ip_address INET,
    clicked_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_urls_user_id
ON urls(user_id);

CREATE INDEX idx_clicks_url_id
ON clicks(url_id);

