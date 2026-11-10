import streamlit as st
from langchain_core.messages import AnyMessage, HumanMessage    
from langgrapg_backned import chatbot 

# with st.chat_message('user'):
#     st.text('hi')

# with st.chat_message("assistant"):
#     st.text("how are you?")
    
# user_input=st.chat_input("Type here")
# if user_input:
#     with st.chat_message("user"):
#         st.text(user_input)
        
# if user_input:
#     with st.chat_message("assistant"):
#         st.text(user_input)


CONFIG={"configurable":{"thread_id":'thread-1'}}

if "message_history" not in st.session_state:
    st.session_state["message_history"]=[]
    
for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message["content"])

user_input=st.chat_input("Type Here")
if user_input:
    st.session_state["message_history"].append({'role':'user', 'content':user_input})
    with st.chat_message("user"):
        st.text(user_input)
        

    response= chatbot.invoke({'messages':[HumanMessage(content=user_input)]}, config=CONFIG) 
    ai_msg=response['messages'][-1].content  
    st.session_state["message_history"].append({'role':'assistant', 'content':ai_msg})
    with st.chat_message("assistant"):
        st.text(ai_msg)