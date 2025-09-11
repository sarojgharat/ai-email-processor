# Email Request Classifier API

This FastAPI project provides CRUD operations for managing email-based business process requests. Each request includes the original email, classification type, and extracted structured data.

## Features

- Create new email request entries
- Read by `request_id`
- Update classification and extracted data
- Delete entries

## Setup

1. Install dependencies:
   ```bash
   cd email_request_service
   uv init --python python
   uv venv
   .venv/bin/activate
   uv add fastapi uvicorn sqlalchemy psycopg2-binary requests
   uv sync --all-groups

   uvicorn main:app --reload --port 8002

- Visit http://localhost:8000/docs
