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
    cd email_processor
    uv init --python python
    uv venv
    .venv/bin/activate
    uv add a2a-sdk uvicorn click google-adk requests google_auth_oauthlib rich
    uv sync --all-groups
    ```

### Basic Usage

To run the agent with the default host (`localhost`) and port (`9999`), simply execute the Python script:

```bash
uv run python -m client

This launches the agent server at `http://localhost:9999`





## ⚙️ Setup & Installation

```bash
git clone 
cd email_processor
uv init --python python
uv venv
.venv/bin/activate
uv add a2a-sdk uvicorn click google-adk requests google_auth_oauthlib rich
uv sync --all-groups
touch .env
echo "GOOGLE_API_KEY=your_key_here" > .env
```

---

## 🧪 Running the Project

### 🟢 Step 1: Start the Agent Server

```bash
uv run python -m client
```
This launches the agent server at `http://localhost:9999`.