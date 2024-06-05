
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
import getpass
from langchain_cohere import CohereEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
inference_api_key = os.getenv('INFERENCE_API_KEY')
groq_api_key = os.getenv("groq_api_key")
cohere_api_key = os.getenv("COHERE_API_KEY")
# llm = ChatCohere(model="command-r")
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
# embeddings = CohereEmbeddings()
embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=inference_api_key,model_name='sentence-transformers/all-MiniLM-l6-v2')

#### loaders  ##############

def loading_youtube(link):
    loader = YoutubeLoader.from_youtube_url(
    link, add_video_info=False
    )
    text = loader.load()  
    return text

def loading_website(link):
    loader = WebBaseLoader(link)
    docs = loader.load()
    return docs

def loading_pdf(pdf):
    loader = PyPDFLoader(pdf)
    pages = loader.load_and_split()
    return pages

########## splitting and storing the embeddings ###########

def splitting_storing(text):    
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(text)
    vector = FAISS.from_documents(documents, embeddings)
    return vector

######## prompt template #############

def prompting():
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
    <context>
    {context}
    </context>
    Question: {input}""")
    return prompt








