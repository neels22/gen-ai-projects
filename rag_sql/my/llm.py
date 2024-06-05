import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

load_dotenv()
openai_api_key = os.getenv("openai_api_key")
groq_api_key = os.getenv("groq_api_key")


def initialize_openai_model():
    """
    Initialize the OpenAI model and return the ChatOpenAI object.
    Requires the OpenAI API key to be set in a .env file.
    """
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        return llm
    except Exception as e:
        print(f"Error initializing OpenAI model: {e}")
        return None



def initialize_groq_model():
    """
    Initialize the Groq model and return the ChatGroq object.
    Requires the Groq API key to be set in a .env file.
    """
    try:        
        llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
        return llm
    except Exception as e:
        print(f"Error initializing Groq model: {e}")
        return None
