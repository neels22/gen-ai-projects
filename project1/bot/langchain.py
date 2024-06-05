


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
    
    user question : {user_question}
 
""")

    # final_answer_prompt.format_messages(user_question=message)
    print(final_answer_prompt)

    chain = final_answer_prompt|Groq_llm|StrOutputParser()

    response = chain.invoke({"user_question":message})
    # print(response)
    return response

