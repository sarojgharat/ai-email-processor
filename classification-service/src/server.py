import click
import logging
from mcp.server.fastmcp import FastMCP
from .classifier import TextClassifier

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--host', default='localhost', help='Host to bind the server to')
@click.option('--port', default=8001, help='Port to run the server on')
def run_server(host, port):
    print("-----------Inside MCP Server------------------")
    # Create MCP Server
    mcp = FastMCP(port=port, host=host)

    @mcp.tool()
    def classify_text(process: str, input_text: str) -> dict:
        """Classify the input_text based on process"""
        logger.info(f"Inside================={process} {input_text}")
        text_classifier = TextClassifier()
        result = text_classifier.classify_text(process, input_text)
        return {
            "process": process,
            "text": input_text,
            "classification_type": result["classification_type"],
            "confidence_score": result["confidence_score"]
        }

    mcp.run(transport="streamable-http", mount_path="/mcp")
    logger.info(f"MCP Server running on {host}:{port}")
    print(f"MCP Server running on {host}:{port}")


if __name__ == "__main__":
    run_server()
