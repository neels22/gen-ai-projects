
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import getpass
import os
from utils import llm,embeddings,loading_youtube,loading_website,loading_pdf,splitting_storing,prompting


llm=llm
embeddings=embeddings

web_link = input("Enter the website link: ")
text = loading_website(web_link)
vector = splitting_storing(text)
prompt = prompting()
document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

while True :
    user_input = input("enter the query: ")
    if user_input =="" or user_input=="exit":
        break
    response = retrieval_chain.invoke({"input": user_input}) 

    print(response["answer"])
