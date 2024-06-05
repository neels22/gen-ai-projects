
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import getpass
import os
from utils import llm,embeddings,loading_youtube,loading_website,loading_pdf,splitting_storing,prompting,similarities_top_k,llm_model_with_tool,output_parser

pdf_path = input("enter the pdf path: ")

text = loading_pdf(pdf_path)
vector = splitting_storing(text)
prompt = prompting()


human_prompt = input("enter your query: ")
prompt_embedding = embeddings.embed_query(human_prompt)

top_k_similar_documents = vector.similarity_search_by_vector(
                    embedding=prompt_embedding,
                    k=similarities_top_k
                )

chain = prompt | llm_model_with_tool | output_parser

response = chain.invoke({
                    "documents": top_k_similar_documents,
                    "input": human_prompt
                })

print("answer: ", response["answer"])
print("sources: ", response["citations"])