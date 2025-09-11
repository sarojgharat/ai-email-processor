CREATE TABLE email_requests (
    request_id TEXT PRIMARY KEY,
    business_process TEXT,
    classification_type TEXT,
    original_email JSONB,
    extracted_data JSONB,
    automation_status TEXT,
    processing_status TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS manual_moves (
    move_id UUID PRIMARY KEY,
    equipment_id VARCHAR(255) NOT NULL,
    from_location VARCHAR(255) NOT NULL,
    to_location VARCHAR(255) NOT NULL,
    moved_by VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);

-- This table stores the main business processes.
CREATE TABLE business_processes (
    id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    description VARCHAR,
    PRIMARY KEY (id),
    UNIQUE (name)
);

-- This table stores the classification categories associated with each business process.
-- The 'process_id' column links each category back to a specific process.
CREATE TABLE classification_categories (
    id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    process_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(process_id) REFERENCES business_processes (id)
);

-- This table defines the specific data fields to be extracted for each category.
-- The 'category_id' links each format to a classification category.
-- The 'format_definition' column would store a JSON object detailing the schema.
CREATE TABLE data_extraction_formats (
    id INTEGER NOT NULL,
    format_name VARCHAR NOT NULL,
    format_definition JSON NOT NULL,
    category_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(category_id) REFERENCES classification_categories (id)
);

