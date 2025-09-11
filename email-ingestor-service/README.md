# Email Processor

Client for calling orchestration agent

## Installation

1.  **Clone the repository** (if applicable):
    ```bash
    cd email_processor
    ```

2.  **Install the required packages**:
    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    cd email-ingestor-service
    uv init --python python
    uv venv
    .venv/bin/activate
    uv add uvicorn click requests google_auth_oauthlib rich
    uv sync --all-groups
    ```

### Basic Usage

To run the email ingestor service, simply execute the Python script:

```bash
uv run python -m client