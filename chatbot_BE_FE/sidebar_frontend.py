import streamlit as st
from langchain_core.messages import AnyMessage, HumanMessage    
from langgrapg_backned import chatbot 
import uuid

#thread id
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

#new chat
def reset_convo():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"]=[]
    
# chat thread
def add_thread(thread_id):
    if thread_id not in st.session_state["chat_thread"]:
        st.session_state["chat_thread"].append(thread_id) 
        
def load_convo(thread_id):
    return chatbot.get_state(config={"configurable":{'thread_id':thread_id}}).values['messages']

# message history store
if "message_history" not in st.session_state:
    st.session_state["message_history"]=[]

if "thread_id" not in st.session_state:
    st.session_state["thread_id"]=generate_thread_id()
    
if "chat_thread" not in st.session_state:
    st.session_state["chat_thread"]=[]
add_thread(st.session_state["thread_id"])


    
# SIDEBAR
st.sidebar.title("LangGraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_convo()
    
st.sidebar.header("My conversation")

for thread_id in st.session_state["chat_thread"]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=load_convo(thread_id)
        
        temp_msg=[]
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_msg.append({'role':role, 'content':message.content})
        st.session_state['message_history']=temp_msg

#  history as a role
for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message["content"])

user_input=st.chat_input("Type Here")
if user_input:
    st.session_state["message_history"].append({'role':'user', 'content':user_input})
    with st.chat_message("user"):
        st.text(user_input)
        

    CONFIG={"configurable":{"thread_id":st.session_state["thread_id"]}}
    
    # st.session_state["message_history"].append({'role':'assistant', 'content':user_input})
    with st.chat_message("assistant"):
        ai_msg=st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
                
            )
        )
        
    st.session_state["message_history"].append({'role':'assistant', 'content':ai_msg})
