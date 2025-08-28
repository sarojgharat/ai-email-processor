# Data Extraction Agent

An agent that extract data in Json format from an unstructured text.

## Installation

1.  **Clone the repository** (if applicable):
    ```bash
    cd data_extraction_agent
    ```

2.  **Install the required packages**:
    It's recommended to use a virtual environment to manage dependencies.

    ```
    cd data_extraction_agent
    uv init --python python
    uv venv
    .venv\Scripts\activate
    uv add mcp mcp[cli] langchain langchain-google-genai fastapi uvicorn
    uv sync --all-groups
    ```

### Basic Usage

To run the agent with the default host (`localhost`) and port (`8888`), simply execute the Python script:

```bash
uv run python -m main

This launches the agent server at `http://localhost:8888`