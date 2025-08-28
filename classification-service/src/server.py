from mcp.server.fastmcp import FastMCP
from .classifier import TextClassifier
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
def classify_text (process: str, input_text: str) -> dict:
    """Classify the input_text based on process"""
    
    logger.info(f"Inside================={process} {input_text}")
    text_classifier = TextClassifier()
    result = text_classifier.classify_text (process, input_text)
    return {
        "process" : process,
        "text" : input_text,
        "classification_type": result["classification_type"],
        "confidence_score": result["confidence_score"]
    }

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse")