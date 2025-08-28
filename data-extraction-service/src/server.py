from mcp.server.fastmcp import FastMCP
from .extractor import DataExtractor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP Server
mcp = FastMCP()

##### Tools #####

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

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse")