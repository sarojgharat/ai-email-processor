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
service = ConfigService("src\\config.json")


if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def extract_text(process: str, category: str, text: str) -> str:
    extraction_format = get_extraction_format(process, category)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that classifies text into categories."),
        ("human", "From the input text: {text}, extract data in the format: '{extraction_format}'")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "text" : text,
        "extraction_format" : extraction_format
    })
    return response.content.strip()

def get_extraction_format(process: str, category: str) -> list[str]:
    output_format_file = service.get_value(process, category)
    print (output_format_file)
    return read_json_value(output_format_file)

def read_json_value(file_path: str) -> str:
    """Read JSON file and return the value for the given key as a string."""
    data=""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
    
if __name__ == '__main__':
    extracted_text = extract_text("booking", "booking amendment" ,"Requesting amendment to booking CMA12345678 on CMA CGM Titan / 0TV1E with revised ETD at Nhava Sheva on 27-Aug-2025, container availability on 22-Aug-2025, updated gross weight of 21,500 kg (previously 20,000 kg); all other details unchanged—please confirm updated booking and revised container release number")
    logger.info(f"Extracted Data: {extracted_text}")