# Chatbot Backend and Frontend Handover

This guide is a handover for the small Streamlit + LangGraph chatbot in
`chatbot_BE_FE/`. It describes what each file does, how a message travels from
the UI to the model and back, how conversation state is retained, how to run
the app, and the current limitations to know before extending it.

## What this project builds

The app is a Python chatbot with two main layers:

- **Frontend:** Streamlit collects text, renders chat bubbles, and keeps a
  display history in `st.session_state`.
- **Backend:** LangGraph keeps message state for a conversation thread and
  runs a single node that sends that thread's messages to a Groq chat model.

There is no separate HTTP API or database in this demo. The frontend imports
and invokes the compiled graph directly in the same Python application.

## Files and responsibilities

| File | Responsibility |
|---|---|
| `chatbot_BE_FE/langgrapg_backned.py` | Loads configuration, creates the Groq model, defines the graph state and model node, adds an in-memory checkpointer, and exports the compiled graph as `chatbot`. The filename is misspelled as `langgrapg_backned.py`; imports and run instructions must use that exact existing name. |
| `chatbot_BE_FE/streamlit_frontend.py` | The default, non-streaming UI. It uses one fixed graph thread ID (`thread-1`), calls `chatbot.invoke()`, and displays the returned answer. |
| `chatbot_BE_FE/streaming_frontend.py` | An alternative UI that streams generated message chunks into the assistant bubble. It also uses the fixed thread ID `thread-1`. |
| `chatbot_BE_FE/sidebar_frontend.py` | An alternative UI with a “New Chat” button and a sidebar list of conversation IDs. It uses one graph thread ID per conversation and reloads a selected thread from the graph checkpointer. |
| `.env` | Local configuration for `GROQ_API_KEY`. Keep the real key out of source control and logs. |
| `requirements.txt` | Python packages needed by the examples, including the Groq integration used by this chatbot. |

The three frontend files are alternatives, not a frontend/backend pair that
must all run together. Start only the frontend you want to use.

## Architecture and message flow

```text
Browser
  │ user types a message
  ▼
Streamlit frontend
  ├─ renders prior st.session_state["message_history"]
  ├─ saves and displays the new user text
  ├─ wraps text in a LangChain HumanMessage
  └─ calls chatbot.invoke(...) or chatbot.stream(...)
          │ input state + configurable thread_id
          ▼
    Compiled LangGraph (chatbot)
      ├─ checkpointer loads state for this thread_id
      ├─ START → chat_node → END
      ├─ add_messages combines new messages with prior messages
      └─ chat_node calls ChatGroq with the conversation messages
              │
              ▼
          Groq model response (AIMessage)
              │ returned graph state / streamed chunks
              ▼
Streamlit extracts or accumulates assistant text,
stores it in the UI history, and renders the reply
```

In the default frontend, each request sends only the newly typed `HumanMessage`.
The LangGraph checkpointer is what makes prior messages available to the model
on later requests for the same thread. The UI's own message list is separate:
it is used to redraw chat bubbles, not passed as the source of model context.

## Backend walkthrough: `langgrapg_backned.py`

### 1. Configuration and model client

The backend calls `load_dotenv()` to load `.env` values into the process
environment. It then constructs:

```python
ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY"),
)
```

The model name selects the provider model, the low temperature favors less
variable responses, and the API key authenticates requests. The key must be
available when the backend module is imported. A missing or invalid key, a
provider/network problem, or an unavailable model will cause the model call to
fail; the app currently does not add a custom error/retry layer.

### 2. Graph state shape

```python
class ChatState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

`ChatState` is the state passed between graph nodes. It contains LangChain
message objects (for example `HumanMessage` and `AIMessage`). The
`add_messages` reducer appends/merges messages returned by a node instead of
replacing the existing message list. This lets the state represent the
conversation over multiple calls to the same thread.

### 3. Model node

`chat_node(state)` reads `state["messages"]`, passes the list to
`model.invoke(messages)`, and returns the model response under the `messages`
key. The returned assistant message is merged into graph state using the
`add_messages` reducer.

### 4. Graph and checkpointing

The graph has one node and a straight-through route:

```text
START → chat_node → END
```

`graph.compile(checkpointer=InMemorySaver())` creates the `chatbot` object
imported by the frontends. `InMemorySaver` retains checkpoints only in the
running Python process. It is not a disk database: restarting the process
clears graph conversations.

For checkpoint continuity, every invocation must pass a stable
`configurable.thread_id`. The graph uses that value to select which
conversation state to load and update.

## Default frontend walkthrough: `streamlit_frontend.py`

1. The frontend imports `chatbot` from `langgrapg_backned.py`.
2. It sets `CONFIG` to `{"configurable": {"thread_id": "thread-1"}}`.
3. On the first Streamlit run in a browser session, it creates an empty
   `st.session_state["message_history"]`.
4. On every rerun, it loops over that list and redraws its user/assistant
   messages.
5. When `st.chat_input()` returns text, it appends and displays the user
   message.
6. It wraps the text in `HumanMessage(content=user_input)` and calls
   `chatbot.invoke({"messages": [...]}, config=CONFIG)`.
7. LangGraph loads the checkpoint for `thread-1`, merges the new user message,
   runs `chat_node`, and saves the updated conversation state.
8. The frontend reads the most recent response from
   `response["messages"][-1].content`, appends that text as an assistant
   message to Streamlit's UI history, and renders it.

The default UI therefore uses request/response behavior: the assistant bubble
appears after the complete model response is returned. The assistant history
currently stores `ai_msg` (the model response), not the user's input.

## Alternative frontend files

### `streaming_frontend.py`

This uses the same basic UI history and fixed `thread-1` as the default
frontend. Instead of `chatbot.invoke()`, it calls
`chatbot.stream(..., stream_mode="messages")`. Streamlit's `st.write_stream()`
renders the model's message chunks as they arrive and returns the accumulated
text, which is then saved as the assistant's UI-history entry.

This is token/chunk streaming to the UI; the graph still has the same
single-node backend and in-memory checkpoint behavior.

### `sidebar_frontend.py`

This version adds a conversation selector:

- It creates a thread ID for the current conversation and tracks IDs in
  `st.session_state["chat_thread"]`.
- “New Chat” creates another ID and clears the displayed
  `message_history`.
- Clicking a listed ID selects it, calls `chatbot.get_state()` for that graph
  thread, and rebuilds the visible history from its saved LangChain messages.
- A new user message is streamed using the selected thread ID, so each listed
  conversation has a separate graph checkpoint.

The sidebar list and selected thread are held in Streamlit session state and
are not a durable conversation index. The graph messages themselves are also
only in the `InMemorySaver` process memory.

## Setup and run

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item env.example .env
```

Edit `.env` and set a valid provider key:

```env
GROQ_API_KEY=your_api_key_here
```

Do not commit the real `.env` file or expose the key in screenshots, logs, or
shared documentation.

Run the default frontend from the repository root:

```powershell
streamlit run .\chatbot_BE_FE\streamlit_frontend.py
```

To try one of the alternatives, substitute
`streaming_frontend.py` or `sidebar_frontend.py` in that command. Open the
local URL printed by Streamlit (typically `http://localhost:8501`).

## State and persistence: what is and is not saved

There are two distinct state stores:

1. **Streamlit `st.session_state`:** keeps the displayed `message_history`
   for that browser's active Streamlit session, and in the sidebar version
   also keeps its thread list/current thread. It is not a permanent store.
2. **LangGraph `InMemorySaver`:** keeps actual graph message state per
   `thread_id` in the running Python process. It is not written to a file or
   database and is cleared when that process restarts.

The default and streaming frontends hard-code the same `thread-1` thread ID.
If multiple browser sessions use the same running app, their backend calls
therefore target the same graph thread even though each browser has separate
Streamlit UI history. This demo is intended for learning/local use, not
multi-user isolation. A production or shared deployment should assign and
authorize a distinct thread ID per user/session, use durable storage if
conversations must survive restarts, and protect the API key and service.

## Current scope and extension points

- **Add graph behavior:** add nodes/edges in `langgrapg_backned.py` and update
  `ChatState` if nodes need additional state. Keep the frontend calling the
  exported compiled `chatbot` graph.
- **Change the model:** adjust the `ChatGroq` configuration and ensure the
  selected model is available for the API account.
- **Add durable history:** replace the in-memory checkpointer with an
  appropriately configured persistent LangGraph checkpointer and manage its
  lifecycle.
- **Improve user isolation:** generate a stable unique thread ID per
  Streamlit session/user rather than sharing `thread-1`.
- **Improve reliability:** add deliberate validation and user-facing error
  handling for missing configuration and provider failures.

The current backend does not expose a REST endpoint, support file uploads,
perform authentication, or persist messages across process restarts.

## Troubleshooting

| Symptom | Likely cause / check |
|---|---|
| Import error for `langchain_groq` | Reinstall dependencies from the repository's `requirements.txt`; confirm `langchain-groq` is included. |
| Authentication error from Groq | Confirm `.env` exists at the repository root, `GROQ_API_KEY` is set correctly, and the key is active. Restart Streamlit after changing environment configuration. |
| Model/provider error | Check network access, model availability, and provider account permissions. |
| `No module named langgrapg_backned` | Run Streamlit with the frontend script path shown above so the `chatbot_BE_FE` directory is on the Python import path; preserve the filename's existing spelling. |
| Conversation disappears after restart | Expected with `InMemorySaver`; it is process memory, not durable storage. |
| Multiple users see context from the same thread | The default frontends use the shared fixed ID `thread-1`; use isolated thread IDs before deploying to multiple users. |

## Quick handover summary

The default app is a direct in-process connection from Streamlit to a compiled
LangGraph graph. Streamlit collects and displays the conversation; LangGraph's
`add_messages` reducer and in-memory checkpointer retain the model context for
the configured thread; one graph node calls Groq and returns the assistant
message. The repository also contains streaming and sidebar versions of the
frontend, but they reuse the same backend. The implementation is a local
learning demo with volatile storage and no user isolation or production
security layer.
