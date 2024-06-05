import uuid
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.utilities import SQLDatabase
from  langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



load_dotenv()

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())

session_id = st.session_state['session_id']

try:
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "sample"
    port = '3306'
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")
except Exception as e:
    print(e)

llm = ChatGroq(
    model='llama3-70b-8192',
    temperature=0
)


def main():
    st.title("SQL Analyzer")
    
    user_input = st.text_input("Enter your text here:")
    
    try:
        prompt_template = """
             - You are an SQL and data visualization expert.
            - Create a syntactically correct {dialect} query. 
            - You have access to the following tables: {table_names}.
            - Your first job is to execute the query according to the user input.
           
            ##INSTRUCTIONS##
            
            1. Your response should be in table format or bar chart data format only nothing else.
            
            2. The column names should be in the same order as the SQL query.
            3. Strictly, the column names are human-readable but with the same meaning as SQL column have. 
            (Example: OPENING_AMT = Opening Amount)
            
            4.Only With table reponse compulsory provide menu to user-
              1.Bar Chart
            
            5. If user select select Bar chart then convert your previous response table into the barchart data format and respond the same nothing else text.
             
            **NOTE**
            1. DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
            
            **Comment**
            - As an data visualization expert you know which data format is required to create the bar chart
            
            HUMAN:
            {input}
        """
        
        prompt = ChatPromptTemplate.from_messages(
        [("system", prompt_template),MessagesPlaceholder(variable_name="chat_history"),("human", "{input}"), MessagesPlaceholder("agent_scratchpad")]
        )
       
        agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", prompt=prompt)
        
        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: SQLChatMessageHistory(session_id=session_id,connection_string="mysql+pymysql://root:root@localhost:3306/sample"),
            input_messages_key="input",
            history_messages_key="chat_history",
        )
    
        response = agent_with_chat_history.invoke({"input":user_input},{"configurable":{"session_id":st.session_state.get('session_id', session_id)}})
        print("Response-",response)
        print("Data Type-",type(response['output']))
        st.write(response['output'])
        
        
        
    except Exception as e:
        print(e,"error is here")

if __name__ == "__main__":
    main()