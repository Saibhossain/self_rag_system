import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import DataFrameLoader

from ingestion.image_processor import process_image


def load_documents(data_path):
    docs = []

    for file in os.listdir(data_path):
        path = os.path.join(data_path, file)

        try:
            # PDF
            if file.endswith(".pdf"):
                pdf_docs = PyPDFLoader(path).load()
                for d in pdf_docs:
                    d.metadata.update({"source": file, "type": "pdf"})
                docs.extend(pdf_docs)

            # Word
            elif file.endswith((".docx", ".doc")):
                word_docs = UnstructuredWordDocumentLoader(path).load()
                for d in word_docs:
                    d.metadata.update({"source": file, "type": "doc"})
                docs.extend(word_docs)

            # Excel
            elif file.endswith(".xlsx"):
                df = pd.read_excel(path)

                for i, row in df.iterrows():
                    text = " | ".join([f"{col}={row[col]}" for col in df.columns])

                    docs.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": file,
                                "type": "excel",
                                "row": int(i)
                            }
                        )
                    )

            # Images
            elif file.lower().endswith((".png", ".jpg", ".jpeg")):
                doc = process_image(path)

                doc.metadata.update({
                    "source": file,
                    "type": "image"
                })

                docs.append(doc)

        except Exception as e:
            print(f"Error processing {file}: {e}")

    print(f"Loaded {len(docs)} documents")
    return docs