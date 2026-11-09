from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import BaseMessage, add_messages
from langgraph.checkpoint.memory import InMemorySaver

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
from typing import TypedDict, Annotated

import time

load_dotenv()


# LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_retries=1,
    timeout=30
)


# Memory
memory = InMemorySaver()


# State
class MessageState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# Chatbot Node
def chatbot_node(state: MessageState):

    print("1. Chatbot node started", flush=True)

    print("2. Sending request to Groq...", flush=True)

    start = time.time()

    response = llm.invoke(state["messages"])

    elapsed = time.time() - start

    print(
        f"3. Groq response received in {elapsed:.2f} seconds!",
        flush=True
    )

    return {
        "messages": [response]
    }


# Graph
graph = StateGraph(MessageState)

graph.add_node("chatbot", chatbot_node)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)


# Compile
chatbot = graph.compile(
    checkpointer=memory
)


# Reusable function for Zentra
def get_chat_response(message, thread_id):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    response = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=message)
            ]
        },
        config=config
    )

    return response["messages"][-1].content
