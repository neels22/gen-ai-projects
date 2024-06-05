from langchain_core.prompts import ChatPromptTemplate

def create_chat_prompt_template(table_info, input_question):
    """
    Create a ChatPromptTemplate object with the provided table information and input question.
    """
    try:
        prompt = ChatPromptTemplate.from_template(f"""
            You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query.
            Never query for all columns from a table. You must query only the columns that are needed to answer the question. 
            Pay attention to use only the column names you can see in the tables 
            below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
            Pay attention to use CURDATE() function to get the current date, if the question involves "today".

            Only use the following tables:
            {table_info}

            Question: {input_question}
            """)
        
        return prompt
    except Exception as e:
        print(f"Error creating ChatPromptTemplate: {e}")
        return None



def second_prompt(final_answer):
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a given a query and the result based on that you have to return an answer in simple English."),
            ("user", f"{final_answer}")
        ])
        return prompt
    except Exception as e:
        print(f"Error creating ChatPromptTemplate: {e}")
        return None


