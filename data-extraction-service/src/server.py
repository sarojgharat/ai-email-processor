import click
import logging
from mcp.server.fastmcp import FastMCP
from .extractor import DataExtractor

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
    def extract_data (process: str, category : str, input_text: str) -> dict:
        """Classify the input_text based on process and category"""
    
        logger.info(f"Inside================={process} {input_text} {category}")
        data_extractor = DataExtractor()
        result = data_extractor.extract_text (process, category, input_text)
        return {
            "process" : process,
            "category" : category,
            "text" : input_text,
            "extracted_data": result
        }

    mcp.run(transport="streamable-http", mount_path="/mcp")
    logger.info(f"MCP Server running on {host}:{port}")
    print(f"MCP Server running on {host}:{port}")


if __name__ == "__main__":
    run_server()
