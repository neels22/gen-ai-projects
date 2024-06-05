
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain import hub
from langchain.agents import AgentExecutor, Tool
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import create_react_agent
from langchain.agents import load_tools
from langchain.memory import ChatMessageHistory

# tools = load_tools(["serpapi"])


load_dotenv()

Groq_llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
search = SerpAPIWrapper()
prompt = hub.pull("hwchase17/react")




tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    )
]
memory = ChatMessageHistory(session_id="test-session")


agent = create_react_agent(Groq_llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)



while True:
        
        user_input = input("enter the query: ")
        if user_input =="exit" or user_input=="":
            break
        print(agent_with_chat_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "<foo>"}},
        )

        )

