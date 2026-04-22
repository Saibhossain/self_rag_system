import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INDEX_PATH = "index/faiss_index"
DATA_PATH = "data/"

MAX_RETRIES = 2

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)