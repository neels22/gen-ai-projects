from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_community.document_loaders import (
    WebBaseLoader, TextLoader, PyPDFLoader, DirectoryLoader
)
from langchain_community.document_loaders import YoutubeLoader
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq

from dotenv import load_dotenv
from typing import List
import os

load_dotenv()


groq_api_key = os.getenv('GROQ_API_KEY')
inference_api_key = os.getenv('INFERENCE_API_KEY')
similarities_top_k = 5


Groq_llm = ChatGroq(temperature=0.0, model_name="mixtral-8x7b-32768")
hugging_embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=inference_api_key,model_name='sentence-transformers/all-MiniLM-l6-v2')



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



def loading_youtube(link):
    try:
        loader = YoutubeLoader.from_youtube_url(link, add_video_info=False)
        text = loader.load()
        return text
    except Exception as e:
        print(f"An error occurred while loading from YouTube: {e}")
        return None

def loading_website(link):
    try:
        loader = WebBaseLoader(link)
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"An error occurred while loading from website: {e}")
        return None

def loading_pdf(pdf):
    try:
        loader = PyPDFLoader(pdf)
        pages = loader.load_and_split()
        return pages
    except Exception as e:
        print(f"An error occurred while loading PDF: {e}")
        return None

def set_directory_loader(directory_path):
    try:
        loader = DirectoryLoader(path=directory_path, show_progress=True)
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"An error occurred while loading from directory: {e}")
        return None
            

def splitting_storing(text):    
    try:
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(text)
        vector = FAISS.from_documents(documents, hugging_embeddings)
        return vector.as_retriever()
    except Exception as e:
        print(f"An error occurred while splitting and storing text: {e}")
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



Groq_llm_model_with_tool = Groq_llm.bind_tools(
            tools=[CitedAnswer],
            tool_choice="CitedAnswer"
        )

output_parser = JsonOutputKeyToolsParser(
            key_name="CitedAnswer", first_tool_only=True
        )























#data model definition 
#citations is a list field containing objects of type Citation. It represents all the document objects referred to in order to answer the user's query.