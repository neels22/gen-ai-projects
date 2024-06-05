
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from utils import llm,embeddings,loading_youtube,splitting_storing,prompting


llm=llm
embeddings=embeddings

yt_link = input("Enter the youtube video link: ")
text = loading_youtube(yt_link)
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
