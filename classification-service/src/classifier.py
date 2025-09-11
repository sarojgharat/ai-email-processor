import os
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from .config_service import ConfigService
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")
logger = logging.getLogger(__name__)


class TextClassifier:

    def __init__(self):

        self.config_service = ConfigService("src\\config.json")

        # Initialize Gemini model
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    def classify_text(self, process: str, text: str) -> dict:
        logger.info (f"Process============{process}") 
        categories = self.get_categories(process)
        logger.info (f"Categories============{categories}") 
    
        prompt = PromptTemplate (
            input_variables = ["categories", "text"],
            template = "Classify the following text into only one of these types: '{categories}'\n\nInput Text: '{text}'"
        )
        
        chain = prompt | self.model
        response = chain.invoke({
            "categories" : categories,
            "text": text
        })
        logger.info (f"Response=========={response}")

        logger.info(f"Confidence Score: {response.response_metadata.get("logprobs")}")
        return {
            "classification_type": response.content.strip(),
            "confidence_score": response.response_metadata.get("logprobs")
    }

    def get_categories(self, process: str) -> list[str]:
        return self.config_service.get_values(process, "categories")