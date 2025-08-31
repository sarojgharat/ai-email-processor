CREATE TABLE email_requests (
    request_id TEXT PRIMARY KEY,
    business_process TEXT,
    classification_type TEXT,
    original_email JSONB,
    extracted_data JSONB,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);