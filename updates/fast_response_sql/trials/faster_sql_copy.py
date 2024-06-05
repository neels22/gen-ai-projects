
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
prompt = ChatPromptTemplate.from_template(template)
db = connect_to_database()


sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | Groq_llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

template = """Based on question, sql query, and sql response, write a natural language response:

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(template)

def run_query(query):
    return db.run(query)


full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=get_schema,
        response=lambda vars: run_query(vars["query"]),
    )
    | prompt_response
    | Groq_llm
)


def main(query):    
    user_question =query
    res = full_chain.invoke({"question": user_question})


    print(res.content)

    return {"answer":res.content}

