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
        

    
    # st.session_state["message_history"].append({'role':'assistant', 'content':user_input})
    with st.chat_message("assistant"):
        ai_msg=st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config={"configurable":{"thread_id":'thread-1'}},
                stream_mode="messages"
                
            )
        )
        
    st.session_state["message_history"].append({'role':'assistant', 'content':ai_msg})
