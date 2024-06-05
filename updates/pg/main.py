from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_community.document_loaders import (
    WebBaseLoader, TextLoader, PyPDFLoader, DirectoryLoader
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from typing import List
import os


groq_api_key = os.getenv('GROQ_API_KEY')
inference_api_key = os.getenv('INFERENCE_API_KEY')

Groq_llm = ChatGroq(temperature=0.0, model_name="llama3-70b-8192")

embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=inference_api_key,model_name='sentence-transformers/all-MiniLM-l6-v2')

collection = "Name of your collection"


class Citation(BaseModel):
    source: str = Field(
        description="source in the metadata of the document object."
    )
    page_content: str = Field(
        description="page_content in the document object.",
    )

class CitedAnswer(BaseModel):

    answer: str = Field(
        description="The answer to the user question, which is based only on the given sources.",
    )
    citations: List[Citation] = Field(
        description="All the Document objects referred to answer the user's query.",
    )


def loading_pdf(pdf):
    try:
        loader = PyPDFLoader(pdf)
        pages = loader.load_and_split()
        return pages
    except Exception as e:
        print(f"An error occurred while loading PDF: {e}")
        return None
    
def prompting():
    try:
        prompt = ChatPromptTemplate.from_template("""Rules:
        You are a quick response generator giving the fastest response possible.
        Answer queries only from the given Documents.
        If any query is asked outside Documents say "I don't know".
        

        Documents:
        {documents}

        User Query:
        {input}""")
        return prompt
    except Exception as e:
        print(f"An error occurred while creating the prompt: {e}")
        return None

llm_model_with_tool = Groq_llm.bind_tools(
            tools=[CitedAnswer],
            tool_choice="CitedAnswer"
        )

output_parser = JsonOutputKeyToolsParser(
            key_name="CitedAnswer", first_tool_only=True
        )



docs = loading_pdf("updates/fast_citations/pdfs/indraneel_offer.pdf")
connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain" 
collection_name = "my_docs"

vectorstore = PGVector.from_documents(
    docs,
    embeddings,
    collection_name=collection,
)