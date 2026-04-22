from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import DataFrameLoader
import pandas as pd

def load_all(file_path):
    if file_path.endswith(".pdf"):
        return PyPDFLoader(file_path).load()
    
    elif file_path.endswith(".docx" or ".doc"):
        return UnstructuredWordDocumentLoader(file_path).load()\
            
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
        return DataFrameLoader(df).load()