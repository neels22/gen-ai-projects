
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import getpass
import os
from utils import llm,embeddings,loading_youtube,loading_website,loading_pdf,splitting_storing,prompting


llm=llm
embeddings=embeddings

pdf_path = input("enter the pdf path: ")

text = loading_pdf(pdf_path)
vector = splitting_storing(text)
prompt = prompting()

document_chain = create_stuff_documents_chain(llm, prompt)
#use of stuff documents chain
#Create a chain for passing a list of Documents to a model.
#Returns An LCEL Runnable
# can pass output parser as well

retriever = vector.as_retriever()
#use of retriever
#By default, the vector store retriever uses similarity search.

 # Returns: VectorStoreRetriever: Retriever class for VectorStore.

# A retriever is an interface that returns documents given an unstructured query. It is more general than a vector store. A retriever does not need to be able to store documents, only to return (or retrieve) them




retrieval_chain = create_retrieval_chain(retriever, document_chain)
#use of chain
#Create retrieval chain that retrieves documents and then passes them on.
#Parameters retriever--- Retriever-like object that returns list of documents. Should either be a subclass of BaseRetriever or a Runnable that returns a list of documents.|||| combine_docs_chain 
#Returns An LCEL Runnable. The Runnable return is a dictionary containing at the very least a context and answer key


# user_input = input("enter the query")
# response = retrieval_chain.invoke({"input": user_input}) 
# # what does it return? ---- runnable with dictionary of context and ans

# print(response["answer"])


while True :
    user_input = input("enter the query: ")
    if user_input =="" or user_input=="exit":
        break
    response = retrieval_chain.invoke({"input": user_input}) 

    print(response["answer"])
