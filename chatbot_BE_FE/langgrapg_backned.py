from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage

load_dotenv()

model=ChatGroq(model="openai/gpt-oss-120b",temperature=0.2,api_key=os.getenv("GROQ_API_KEY"))

class ChatState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]
    
    
    
def chat_node(state:ChatState):
    messages=state['messages']
    response= model.invoke(messages)
    return{"messages":[response]}


checkpointer=InMemorySaver()
graph= StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot=graph.compile(checkpointer=checkpointer)

# stream= chatbot.stream(
#     {'messages':[HumanMessage(content="What is receipe of paste")]},
#     CONFIG={"configurable":{"thread_id":'thread-1'}},
#     stream_mode="messages"
# )

# print(type(stream))

# for message_chunk, metadata in chatbot.stream(
#     {'messages':[HumanMessage(content="What is receipe of paste")]},
#     config={"configurable":{"thread_id":'thread-1'}},
#     stream_mode="messages"
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)