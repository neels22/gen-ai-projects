import pymupdf
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
from langchain_cohere import CohereEmbeddings
from operator import itemgetter
from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI
openai_api_key = os.getenv("openai_api_key")
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser


groq_api_key = os.getenv("groq_api_key")
# cohere_api_key = os.getenv("COHERE_API_KEY")
# llm = ChatCohere(model="command-r")
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")

# embed = CohereEmbeddings()




doc = pymupdf.open("rag_citations\\my\\pdf_for_rag.pdf") 


formatted_list = []

for i, page in enumerate(doc):
    formatted = f"Page number: {i+1} \n page content: {page.get_text()}"
    formatted_list.append(formatted)

print(formatted_list)
# now i have list of documents you can say 

result =  " " + " ".join(formatted)

print(result)




prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a helpful AI assistant. Given a user question and pdf snippets, answer the user question. If none of the snippets answer the question, just say you don't know.\n\nHere are the snippets:{context}",
        ),
        ("human", "{question}"),
    ]
)






vectorstore = FAISS.from_texts(
    result, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()
# template = """Answer the question based only on the following context:
# {context}

# Question: {question}
# """
# prompt = ChatPromptTemplate.from_template(template)
# model = ChatOpenAI()

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(retrieval_chain.invoke("what is black mountain?"))






# #this is a tool
# class cited_answer(BaseModel):
#     """Answer the user question based only on the given sources, and cite the sources used."""

#     answer: str = Field(
#         ...,
#         description="The answer to the user question, which is based only on the given sources.",
#     )
#     citations: List[int] = Field(
#         ...,
#         description="The integer IDs of the SPECIFIC sources which justify the answer.",
#     )


# # binding additional tools to the llm 
# llm_with_tool = llm.bind_tools(
#     [cited_answer],
#     tool_choice="cited_answer",
# )


# output_parser = JsonOutputKeyToolsParser(key_name="cited_answer", first_tool_only=True)



# answer_1 = prompt | llm_with_tool | output_parser
# chain_1 = (
#     RunnableParallel(question=RunnablePassthrough())
#     .assign(context=result)
#     .assign(cited_answer=answer_1)
#     .pick(["cited_answer"])
# )
# print("#"*100)
# res = chain_1.invoke("what is black mountain")

# print(res['cited_answer']['answer'] )

# print(res['cited_answer']['citations'])


# print("#"*100)
