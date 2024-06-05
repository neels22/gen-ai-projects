from utils_copy import (
    
    hugging_embeddings,
    loading_youtube,
    loading_website,
    loading_pdf,
    splitting_storing,
    prompting,
    similarities_top_k,
    Groq_llm_model_with_tool,
    output_parser
)
from langchain_community.document_loaders import (
    WebBaseLoader, TextLoader, PyPDFLoader, DirectoryLoader
)
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.pydantic_v1 import BaseModel, Field
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



pdf = input('enter pdf path: ')
def loading_pdf(pdf):
    try:
        loader = PyPDFLoader(pdf)
        pages = loader.load()
        return pages
    except Exception as e:
        print(f"An error occurred while loading PDF: {e}")
        return None




docs = loading_pdf(pdf)
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, hugging_embeddings)



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


Groq_llm_model_with_tool = Groq_llm.bind_tools(
            tools=[CitedAnswer],
            tool_choice="CitedAnswer"
        )

output_parser = JsonOutputKeyToolsParser(
            key_name="CitedAnswer", first_tool_only=True
        )




prompt = ChatPromptTemplate.from_template(
    """ You are a quick response generator giving the fastest response possible.
        Answer queries only from the given Documents.
        If any query is asked outside Documents say "I don't know".
        

        Documents:
        {context}

        User Query:
        {input}""")



retriever = vector.as_retriever()
response_chain = (
    {"context":retriever,"input":RunnablePassthrough()}
    |prompt
    |Groq_llm_model_with_tool
    |output_parser
)


user_query = input("enter your query: ")

response = response_chain.invoke(user_query)
print( response["answer"],"\n\n\n",response["citations"])
print("\n")
