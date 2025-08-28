import os
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from .config_service import ConfigService
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")


class DataExtractor:

    def __init__(self):
        self.config_service = ConfigService("src\\config.json")
        # Initialize Gemini model
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    def extract_text(self, process: str, category: str, text: str) -> str:
        extraction_format = self.get_extraction_format(process, category)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that classifies text into categories."),
            ("human", "From the input text: {text}, extract data in the format: '{extraction_format}'")
        ])

        chain = prompt | self.model
        response = chain.invoke({
            "text" : text,
            "extraction_format" : extraction_format
        })
        return response.content.strip()

    def get_extraction_format(self, process: str, category: str) -> list[str]:
        output_format_file = self.config_service.get_value(process, category)
        print (output_format_file)
        return self.read_json_value(output_format_file)

    def read_json_value(self, file_path: str) -> str:
        """Read JSON file and return the value for the given key as a string."""
        data=""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data