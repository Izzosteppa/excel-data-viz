-- Create database
CREATE DATABASE IF NOT EXISTS financial_data;
USE financial_data;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create financial_records table
CREATE TABLE IF NOT EXISTS financial_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    year INT NOT NULL,
    month VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Insert sample users
INSERT INTO users (name) VALUES 
('Jane Doe'),
('John Smith'),
('Alice Johnson'),
('Bob Wilson'),
('Sarah Davis');

-- Create indexes for better performance
CREATE INDEX idx_user_year ON financial_records(user_id, year);
CREATE INDEX idx_year_month ON financial_records(year, month);