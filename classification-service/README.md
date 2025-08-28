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

To run the agent with the default host (`localhost`) and port (`7777`), simply execute the Python script:

```bash
uv run python -m main

This launches the agent server at `http://localhost:7777`