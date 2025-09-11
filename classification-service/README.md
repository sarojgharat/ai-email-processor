# Text Classification Agent

An agent that classifies text into predefined categories.

## Installation

1.  **Clone the repository** (if applicable):
    ```bash
    cd classification-service
    ```

2.  **Install the required packages**:
    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    cd classification-service
    uv init --python python
    uv venv
    .venv\Scripts\activate
    uv add mcp[cli] mcp langchain langchain-google-genai fastapi uvicorn
    uv sync --all-groups
    ```

### Basic Usage

To run the text classification api with the default host (`localhost`) and port (`8001`), simply execute the Python script:
```bash
uvicorn src.api.classifier_api:app --host localhost --port 8001

To expose the classification method as a tool on the MCP Server, run the below Python script.
```bash
uv run python -m src.mcp.classifier_mcp_server  --host localhost --port 8002

This launches the agent server at `http://localhost:8001/classify`


python start_services.py --host localhost --port1 9001 --port2 9002