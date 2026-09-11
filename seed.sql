-- Inserts sample/test data

-- ============================
-- URL SHORTENER SAMPLE DATA
-- ============================

-- Insert sample users
INSERT INTO users (name, email)
VALUES
    ('Sunaina', 'sunaina@example.com'),
    ('Rahul', 'rahul@example.com'),
    ('Aman', 'aman@example.com');


-- Insert sample URLs
INSERT INTO urls (short_code, original_url, user_id)
VALUES
    ('abc123', 'https://google.com', 1),
    ('xyz789', 'https://github.com', 1),
    ('pqr456', 'https://youtube.com', 2),
    ('mno111', 'https://kubernetes.io', 3);


-- Insert sample clicks
INSERT INTO clicks (url_id, ip_address)
VALUES
    (1, '192.168.1.10'),
    (1, '192.168.1.20'),
    (1, '192.168.1.30'),
    (2, '192.168.1.40'),
    (2, '192.168.1.50');