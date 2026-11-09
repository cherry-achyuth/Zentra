from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import BaseMessage,add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,AIMessage
from dotenv import load_dotenv
from typing import TypedDict,Annotated


load_dotenv()

##llm = ChatGoogleGenerativeAI(model = "gemini-3.8-flash",temperature = 0)
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_retries=1,
    timeout=30
)
memory = InMemorySaver()

class MessageState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def chatbot(state:MessageState):
    print("1. Chatbot node started")

    print("2. Sending request to Gemini...")
    response = llm.invoke(state["messages"])

    print("3. Gemini response received!")
    return {'messages':[response]}

graph =  StateGraph(MessageState)

graph.add_node('chatbot',chatbot)

graph.add_edge(START,'chatbot')
graph.add_edge('chatbot',END)

chatbot =  graph.compile(checkpointer = memory)
'''
while True:
    thread_id = 1
    config = {'configurable':{'thread_id':thread_id}}
    msg = input("type your message: ")
    if msg.strip().lower() in ['exit','bye','quit']:
        break

    for response,metadata in chatbot.stream(
        {"messages" : [HumanMessage(msg)]},
        config = config,stream_mode='messages'):
        print(response.content)
'''