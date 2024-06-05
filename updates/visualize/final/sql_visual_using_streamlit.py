

import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st



groq_api_key = os.getenv("groq_api_key")
Groq_llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")


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


def get_schema(_):
    schema = db.get_table_info()
    return schema




template = """
you are a sql query expert.
#important#
1.only return the sql query generated
2.no other text should be returned
3.make sure the query is correct in syntax
4.Don't use the "SQL Query:" in the response so that only query can be returned
5.Strictly, the column names are human-readable but with the same meaning as SQL column have (Example: OPENING_AMT = Opening Amount)

Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
Give the response in following format:

SQL Query: 

"""


query_generation_prompt = ChatPromptTemplate.from_template(template)
db = connect_to_database()

sql_query_generation_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | query_generation_prompt
    | Groq_llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)


final_answer_prompt = ChatPromptTemplate.from_template("""
    you will be provided with a query along with its response from sql database.
    You have to provide its answer in simple english.
    user query:{query}
    sql response generated:{response}
    #instructions#
    1. give answer in simple english based on the query and response 
 
""")




def main(query):    
    user_query =query
    SQL_query = sql_query_generation_chain.invoke({"question": user_query})
    print(SQL_query)
    db_query_response = db.run(SQL_query)
    print(db_query_response)
 

    simple_english_chain = final_answer_prompt | Groq_llm | StrOutputParser()
    english_response = simple_english_chain.invoke({"query":user_query,"response":db_query_response})


    print("query executed: ",db_query_response,"\n answer: ",english_response)
    print("#"*10)

    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "sample"
    port = '3306'

    try:
        # Create an SQLAlchemy engine
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")
       
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")


    df = pd.read_sql(SQL_query,engine)
    print(df) 
    print("\n")
    print("****************")

    st.bar_chart(df)


if __name__=='__main__':
    
    user_query = input("enter query: ")
    main(user_query)


