from django.shortcuts import render
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv


load_dotenv()
groq_api_key = os.getenv("groq_api_key")



def askbot(message):
    Groq_llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    final_answer_prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant.You have to answer question from the user
    
    user question : {user_question}""")
    chain = final_answer_prompt|Groq_llm|StrOutputParser()

    response = chain.invoke({"user_question":message})
    return response




def ai_response(message):
    pass


def chat(request):
    if request.method=="POST":
        message = request.POST.get('message')
        response = askbot(message)
        return response

  
    return render(request,'chatbot.html')
    

