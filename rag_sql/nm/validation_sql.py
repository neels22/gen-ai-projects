from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import SQLDatabase
from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq


groq_api_key = os.getenv("groq_api_key")
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
# embeddings = CohereEmbeddings(model="embed-english-light-v3.0")

from langchain_openai import ChatOpenAI
openai_api_key = os.getenv("openai_api_key")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

db_user = "root"
db_password = "root"
db_host = "localhost"
db_name = "sample"
port = '3306'

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")

print('#'*100)


######












from langchain.chains import create_sql_query_chain
chain = create_sql_query_chain(llm, db)

system = """Double check the user's {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only."""
prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{query}")]
).partial(dialect=db.dialect)
validation_chain = prompt | llm | StrOutputParser()

full_chain = {"query": chain} | validation_chain

user_inp = input("enter you query")

query = full_chain.invoke(
    {
        "question": user_inp
    }
)
print(query)

print(db.run(query))