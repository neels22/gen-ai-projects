import os
import getpass
from utils import llm, embeddings, loading_youtube, loading_website, loading_pdf, splitting_storing, prompting, similarities_top_k, llm_model_with_tool, output_parser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

def load_text_from_pdf(pdf_path):
  
    text = loading_pdf(pdf_path)
    return text


def load_text_from_website(website_link):
  
    text = loading_website(website_link)
    return text

def load_text_from_youtube(youtube_link):

    text = loading_youtube(youtube_link)
    return text

def get_prompt_embedding(human_prompt):
 
    return embeddings.embed_query(human_prompt)

def find_top_k_similar_documents(vector, prompt_embedding):

    return vector.similarity_search_by_vector(embedding=prompt_embedding, k=similarities_top_k)

def generate_response(prompt, llm_model_with_tool, output_parser, documents, input_text):

    chain = prompt | llm_model_with_tool | output_parser
    return chain.invoke({"documents": documents, "input": input_text})


def main():


    choice = int(input("choose\n 1.PDF \n 2.Website \n 3.Youtube vid:\n "))

    if choice==1:
         pdf_path = input("Enter the PDF path: ")
         text = load_text_from_pdf(pdf_path)
    elif choice==2:
        web_link = input("enter the webiste link: ")
        text = load_text_from_website(web_link)
    elif choice==3:
        youtube_link = input("enter the youtube link: ")
        text = load_text_from_youtube(youtube_link)
    else:
        print("enter valid input.")
        


    vector = splitting_storing(text)
    while True:
        human_prompt = input("Enter your query: ")
        if human_prompt =='exit' or human_prompt=='':
            break
        prompt_embedding = get_prompt_embedding(human_prompt)

        top_k_similar_documents = find_top_k_similar_documents(vector, prompt_embedding)

        response = generate_response(prompting(), llm_model_with_tool, output_parser, top_k_similar_documents, human_prompt)

        print("Answer:", response["answer"])
        print("Sources:", response["citations"])

if __name__ == "__main__":
    main()
