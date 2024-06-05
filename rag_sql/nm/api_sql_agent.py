
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.prompts import MessagesPlaceholder



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

db = connect_to_database()



system = """   - You are an SQL  expert.
            - Create a syntactically correct {dialect} query. 
            - You have access to the following tables: {table_names}.
            - Your first job is to execute the query according to the user input.
           
            ##INSTRUCTIONS##
            
            1. Your response should be in proper format only nothing else.
            
            2. The column names should be in the same order as the SQL query.
            3. Strictly, the column names are human-readable but with the same meaning as SQL column have. 
            (Example: OPENING_AMT = Opening Amount)
  
            **NOTE**
            1. DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
            
            
            HUMAN:
            {input}

"""


prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{input}"),(MessagesPlaceholder(variable_name="agent_scratchpad"))]
).partial(dialect=db.dialect)

agent_executor = create_sql_agent(Groq_llm, db=db,agent_type="openai-tools", prompt=prompt)



def main(query):
    user_input = query
    if user_input=="exit" or user_input=="":
        exit()
    response=agent_executor.invoke(user_input)

    return response['output']