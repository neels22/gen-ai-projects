from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
load_dotenv()



Groq_llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

conversation = ConversationChain(
    llm=Groq_llm,
    verbose=True,
    memory=ConversationBufferMemory()
)

while True:
    user_input = input("enter query: ")
    if user_input=="exit" or user_input == "":
        break
        
    response = conversation.predict(input=user_input)

    print(response)
