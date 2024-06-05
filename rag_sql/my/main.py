from llm import initialize_openai_model,initialize_groq_model
from db_connect import initialize_database
from prompt import create_chat_prompt_template,second_prompt
from langchain_core.output_parsers import StrOutputParser


llm = initialize_openai_model()
llm2 = initialize_groq_model()
db, schema = initialize_database()
output_parser = StrOutputParser()
output_parser2 = StrOutputParser()

# prompt2 = second_prompt(final_answer)



while(True):
    query = input("enter your query: ")
    prompt = create_chat_prompt_template(schema, query)
    chain = prompt | llm | output_parser 
    sql_query_generated=chain.invoke({"table_info":schema,"input":query})
    print(sql_query_generated)
    # print(db.run(sql_query_generated))
    query_result = db.run(sql_query_generated)
    print(query_result)

    prompt2 = second_prompt(sql_query_generated+query_result)
    chain2 = prompt2 | llm2 | output_parser2
    response  = chain2.invoke({"input":sql_query_generated+query_result})
    print(response)


