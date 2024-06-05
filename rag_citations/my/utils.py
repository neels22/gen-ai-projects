from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
from langchain_cohere import CohereEmbeddings
from operator import itemgetter
from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from  langchain.chains import create_citations_fuzzy_match_chain

from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser

groq_api_key = os.getenv("groq_api_key")

groq_api_key = os.getenv("groq_api_key")
cohere_api_key = os.getenv("COHERE_API_KEY")
# llm = ChatCohere(model="command-r")
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
# embeddings = CohereEmbeddings()
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
wiki = WikipediaRetriever(top_k_results=6, doc_content_chars_max=2000)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a helpful AI assistant. Given a user question and some Wikipedia article snippets, answer the user question. If none of the articles answer the question, just say you don't know.\n\nHere are the Wikipedia articles:{context}",
        ),
        ("human", "{question}"),
    ]
)

print("#"*100)

prompt.pretty_print()
print("#"*100)




#this is a tool
class cited_answer(BaseModel):
    """Answer the user question based only on the given sources, and cite the sources used."""

    answer: str = Field(
        ...,
        description="The answer to the user question, which is based only on the given sources.",
    )
    citations: List[int] = Field(
        ...,
        description="The integer IDs of the SPECIFIC sources which justify the answer.",
    )


# binding additional tools to the llm 
llm_with_tool = llm.bind_tools(
    [cited_answer],
    tool_choice="cited_answer",
)




output_parser = JsonOutputKeyToolsParser(key_name="cited_answer", first_tool_only=True)


def format_docs_with_id(docs: List[Document]) -> str:
    formatted = [
        f"Source ID: {i}\nArticle Title: {doc.metadata['title']}\nArticle Snippet: {doc.page_content}"
        for i, doc in enumerate(docs)
    ]
    return "\n\n" + "\n\n".join(formatted)


format_1 = itemgetter("docs") | RunnableLambda(format_docs_with_id)


answer_1 = prompt | llm_with_tool | output_parser
chain_1 = (
    RunnableParallel(question=RunnablePassthrough(), docs=wiki)
    .assign(context=format_1)
    .assign(cited_answer=answer_1)
    .pick(["cited_answer", "docs"])
)
print("#"*100)
res = chain_1.invoke("How fast are cheetahs?")

print(res['cited_answer']['answer'] )

print(res['cited_answer']['citations'])


print("#"*100)
