# Orchestration Agent

An agent that delegates to classification and data extraction task to other agents.

## Installation

1.  **Clone the repository** (if applicable):
    ```bash
    cd orchestration_agent
    ```

2.  **Install the required packages**:
    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    cd email-processing-agent
    uv init --python python
    uv venv
    .venv/bin/activate
    uv add a2a-sdk langchain langgraph google-genai httpx python-dotenv langchain-google-genai uvicorn click rich google-adk litellm yfinance google-api-python-client google-auth-httplib2 google-auth-oauthlib google-cloud-aiplatform
    uv sync --all-groups
    ```

### Basic Usage

To run the agent with the default host (`localhost`) and port (`9999`), simply execute the Python script:

```bash
adk web

This launches the agent server at `http://localhost:9999`