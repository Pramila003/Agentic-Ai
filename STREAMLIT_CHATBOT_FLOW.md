# Streamlit Chatbot Flow Guide

This document explains how the chatbot works end-to-end, how the files are connected, and how the data moves between the frontend UI and the LangGraph backend.

## 1. Project files involved

- `chatbot_BE_FE/langgrapg_backned.py`  
  This is the backend file. It defines the LangGraph chatbot, the state, and the model call.

- `chatbot_BE_FE/streamlit_frontend.py`  
  This is the frontend file. It creates the Streamlit chat interface and sends user messages to the backend.

- `.env`  
  This stores the API key used by the model, such as `GROQ_API_KEY`.

## 2. High-level idea

The flow is:

1. A user types a message in the Streamlit app.
2. The Streamlit app stores it in session state.
3. The app sends the message to the LangGraph backend as a `HumanMessage`.
4. The backend graph calls the LLM (`ChatGroq`).
5. The response is returned as an AI message.
6. The frontend displays the AI reply in the chat UI.

In simple words: the frontend handles the UI, and the backend handles the actual AI logic.

## 3. Backend file: `langgrapg_backned.py`

### 3.1 Imports

The backend imports:

```python
from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage
```

These are important:

- `StateGraph` and `START`, `END` are used to build the LangGraph workflow.
- `add_messages` helps merge message lists correctly.
- `ChatGroq` connects the app to Groq's LLM service.
- `InMemorySaver` stores checkpoint/state in memory while the graph runs.
- `load_dotenv()` loads environment variables from `.env`.
- `AnyMessage` is used for the typed message structure.

### 3.2 Loading environment variables

```python
load_dotenv()
```

This reads the `.env` file and loads variables like `GROQ_API_KEY` into the Python environment.

### 3.3 Setting up the model

```python
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)
```

This creates the LLM client object.

- `model`: tells LangChain which Groq model to use.
- `temperature=0.2`: keeps responses relatively stable and focused.
- `api_key=os.getenv("GROQ_API_KEY")`: reads the Groq API key from the environment.

If the key is not set, the model cannot authenticate with Groq.

### 3.4 Defining the graph state

```python
class ChatState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

This defines the state of the graph.

- `messages` is a list of messages.
- `Annotated[...]` with `add_messages` tells LangGraph how to merge chat messages when the graph updates state.

This is the core of a chat workflow: the graph stores the conversation history and passes it through the model.

### 3.5 The main node function

```python
def chat_node(state: ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}
```

This function does the actual AI work:

- It reads the current conversation from `state['messages']`.
- It calls `model.invoke(messages)`.
- The model returns a response object (usually an AIMessage).
- The function stores that response back into the state under `messages`.

This is the central backend logic: pass conversation history to the LLM and return the LLM answer.

### 3.6 Building the graph

```python
checkpointer = InMemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
```

This creates a minimal graph:

- `chat_node` is the single node where the LLM is called.
- `START -> chat_node` means the workflow starts there.
- `chat_node -> END` means after that node finishes, the workflow ends.

Then the graph is compiled:

```python
chatbot = graph.compile(checkpointer=checkpointer)
```

So `chatbot` is the final callable graph object that the frontend can invoke.

## 4. Frontend file: `streamlit_frontend.py`

### 4.1 Imports

```python
import streamlit as st
from langchain_core.messages import AnyMessage, HumanMessage
from langgrapg_backned import chatbot
```

This connects the UI to the backend:

- `streamlit` is used to create the chat interface.
- `HumanMessage` is the message type used to send a user input into the graph.
- `from langgrapg_backned import chatbot` imports the compiled graph object from the backend file.

This is the key connection between the files.

### 4.2 Chat configuration

```python
CONFIG = {"configurable": {"thread_id": "thread-1"}}
```

This config tells LangGraph which conversation thread to use.

- `thread_id` identifies the conversation state.
- Without this, the app would not have a stable thread context in the graph.

### 4.3 Message history in session state

```python
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
```

This creates a storage variable for all previous chat messages.

- It prevents the chat from resetting every time the app re-renders.
- It keeps the UI history persistent across interactions.

### 4.4 Rendering previous messages

```python
for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message["content"])
```

This loops through saved messages and displays them in the Streamlit chat window.

- `role` can be `user` or `assistant`.
- `content` is the text shown in the chat bubble.

### 4.5 Taking new user input

```python
user_input = st.chat_input("Type Here")
```

This waits for the user to type a new message in the Streamlit chat box.

### 4.6 Sending the message to the backend

```python
if user_input:
    st.session_state["message_history"].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)
```

This does two things:

1. Saves the user message to local chat history.
2. Displays the user's message in the UI.

Then the application calls the backend:

```python
response = chatbot.invoke(
    {'messages': [HumanMessage(content=user_input)]},
    config=CONFIG
)
```

This is the most important connection between UI and backend.

What happens here:

- It creates a `HumanMessage` from the text typed by the user.
- It sends it into the LangGraph graph as the input payload.
- `config=CONFIG` tells the graph which thread/interaction state to use.
- The backend runs the model and returns a conversation response object.

### 4.7 Reading the AI response

```python
ai_msg = response['messages'][-1].content
```

The response from the graph is a dictionary with message history. The latest message is the model output.

- `response['messages']` is a list of message objects.
- `[-1]` means the most recent message.
- `.content` extracts the actual text of the assistant reply.

### 4.8 Showing the assistant reply

```python
st.session_state["message_history"].append({'role': 'assistant', 'content': user_input})
with st.chat_message("assistant"):
    st.text(ai_msg)
```

There is a bug here: the assistant chat history stores `user_input` instead of `ai_msg`.

The correct version should be:

```python
st.session_state["message_history"].append({'role': 'assistant', 'content': ai_msg})
```

This means the assistant reply is saved correctly in the history and displayed in the chat UI.

## 5. How the files are connected

The connection is straightforward:

- `streamlit_frontend.py` imports `chatbot` from `langgrapg_backned.py`.
- The frontend creates a `HumanMessage` using the user text.
- It calls `chatbot.invoke(...)`.
- The backend graph executes `chat_node`, which calls the Groq model.
- The model returns an AI response.
- The frontend extracts `.content` and prints it in Streamlit.

So the actual data flow is:

```text
User types text in Streamlit
        ↓
streamlit_frontend.py
        ↓
HumanMessage(content=user_input)
        ↓
chatbot.invoke(...)
        ↓
LangGraph graph -> chat_node -> model.invoke(messages)
        ↓
AIMessage response
        ↓
response['messages'][-1].content
        ↓
Streamlit UI displays assistant reply
```

## 6. Full execution flow

A complete request looks like this:

1. The app loads.
2. `st.session_state["message_history"]` is created if missing.
3. Old messages are displayed.
4. User enters a new message.
5. The frontend appends the user message to session state.
6. The frontend builds a `HumanMessage`.
7. It calls `chatbot.invoke(...)` on the backend graph.
8. The backend graph runs `chat_node`.
9. `chat_node` invokes `model.invoke(messages)`.
10. Groq returns a response.
11. The response is stored into state.
12. The frontend takes the last message content.
13. The app shows the AI answer inside the Streamlit chat panel.

## 7. Why this design is useful

This project separates concerns cleanly:

- The backend is responsible for model interaction and graph state.
- The frontend is responsible for user interface and interaction.
- LangGraph manages state and messages between nodes.
- Streamlit provides a quick UI without building a full web app.

This is a simple and effective template for beginner chatbot projects.

## 8. Important implementation notes

### 8.1 Environment setup

The app needs:

```env
GROQ_API_KEY=your_api_key_here
```

Otherwise the `ChatGroq` client cannot connect to Groq.

### 8.2 Dependency requirements

The project requires packages such as:

- `langchain`
- `langgraph`
- `python-dotenv`
- `streamlit`
- `langchain-groq`

### 8.3 One bug to fix

In `streamlit_frontend.py`, this line stores the wrong value into the chat history:

```python
st.session_state["message_history"].append({'role': 'assistant', 'content': user_input})
```

It should store the model response instead:

```python
st.session_state["message_history"].append({'role': 'assistant', 'content': ai_msg})
```

This is important because otherwise the assistant chat history contains the user input instead of the AI output.

## 9. Summary

This project is a minimal chat application built with:

- Streamlit for the user interface
- LangGraph for workflow/state management
- Groq LLM via `ChatGroq` for responses
- `HumanMessage` and `AIMessage` for conversation data

The core concept is: user input goes into the graph, the graph calls the model, and the model output is displayed in the UI.

This is a clean beginner-friendly example of connecting a frontend to an LLM backend with stateful orchestration.
