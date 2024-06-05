import os
import getpass
from utils import (
    llm,
    embeddings,
    loading_youtube,
    loading_website,
    loading_pdf,
    splitting_storing,
    prompting,
    similarities_top_k,
    llm_model_with_tool,
    output_parser
)


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

class DocumentProcessor:
    def __init__(self):
        self.vector = None  # Initialize vector to ensure it is always defined

    def load_text_from_pdf(self, pdf_path):
        text = loading_pdf(pdf_path)
        return text

    def load_text_from_website(self, website_link):
        text = loading_website(website_link)
        return text

    def load_text_from_youtube(self, youtube_link):
        text = loading_youtube(youtube_link)
        return text

    def splitting_storing(self, text):
        return splitting_storing(text)

    def prompting(self):
        return prompting()

    def llm_model_with_tool(self):
        return llm_model_with_tool

    def output_parser(self):
        return output_parser

    def main(self, choice, path):
        if choice == 1:
            pdf_path = path
            text = self.load_text_from_pdf(pdf_path)
            self.vector = self.splitting_storing(text)
        elif choice == 2:
            web_link = path
            text = self.load_text_from_website(web_link)
            self.vector = self.splitting_storing(text)
        elif choice == 3:
            youtube_link = path
            text = self.load_text_from_youtube(youtube_link)
            self.vector = self.splitting_storing(text)
        else:
            print("Enter valid input.")
            return "Invalid input", []

        if self.vector is None:
            print("Failed to process the input properly.")
            return "Processing error", []



    def human_query_response(self, query):
        human_prompt = query
        if human_prompt == 'exit' or human_prompt == '':
            return "No query provided", []

        prompt_embedding = get_prompt_embedding(human_prompt)
        top_k_similar_documents = find_top_k_similar_documents(self.vector, prompt_embedding)
        response = generate_response(self.prompting(), self.llm_model_with_tool(), self.output_parser(), top_k_similar_documents, human_prompt)

        return response["answer"], response["citations"]

