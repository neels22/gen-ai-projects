

import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import ChatPromptTemplate



groq_api_key = os.getenv("groq_api_key")
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

# openai_api_key = os.getenv("openai_api_key")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)



def connect_to_database():
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "sample"
    port = '3306'

    try:
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")
        return db
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None


def create_answer_prompt():
    try:
        answer_prompt = PromptTemplate.from_template(
            """Based on the schema table below, questions, sql query and sql response, write a natural language response: {schema}

        Question: {question}
        SQL Query: {query}
        SQL Response: {response}
 """
        )
        return answer_prompt
    except Exception as e:
        print(f"An error occurred while creating the answer prompt: {e}")
        return None
    


db = connect_to_database()
answer_prompt = create_answer_prompt()

prompt1 = PromptTemplate.from_template(
   """ Based on the table schema below, write a sql query that would answer the users question.
    {schema}. 

    #Important# 
        1. Your response should be only the SQL Query. 
        2. In the response there should be no other words than the sql query.
        3. Don't write '\' in response


    Question: {question}"""
)

write_query = create_sql_query_chain(llm, db,prompt=prompt1)


print("########################")
user_inp1 = input("enter your input")
response = write_query.invoke({"question":user_inp1,"table_info":db.get_table_info(),"top_k":4})
print(response)
print("###############################")

execute_query = QuerySQLDataBaseTool(db=db)

answer = answer_prompt | llm | StrOutputParser() 

chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
) 


while True:
    user_inp = input("enter the question: ")
    if user_inp == "exit":
        break
    print(chain.invoke({"question": user_inp}))


    