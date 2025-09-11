# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install uv and sync dependencies
RUN pip install uv && uv sync --all-groups

# Copy the rest of the application code
COPY . .

# Expose both service ports
EXPOSE 8001
EXPOSE 8002

# Default command to run both services with externalized host/ports
CMD ["python", "start_services.py", "--host", "0.0.0.0", "--port1", "8001", "--port2", "8002"]