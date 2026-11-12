from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
import os
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage
import sqlite3

load_dotenv()

model=ChatGroq(model="openai/gpt-oss-120b",temperature=0.2,api_key=os.getenv("GROQ_API_KEY"))

class ChatState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]
    
    
    
def chat_node(state:ChatState):
    messages=state['messages']
    response= model.invoke(messages)
    return{"messages":[response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)

graph= StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot=graph.compile(checkpointer=checkpointer)
# CONFIG={"configurable":{"thread_id":'thread-2'}}
# response=chatbot.invoke(
#                 {'messages':[HumanMessage(content="now tell me what is my name ")]},
#                 config=CONFIG
                
#             )
# print(response)

# res=checkpointer.list(None)
# print(res)

def retrive_thread():
    all_thread=set()
    for checkpoint in checkpointer.list(None):
        all_thread.add(checkpoint.config["configurable"]["thread_id"])
        
    return list(all_thread)