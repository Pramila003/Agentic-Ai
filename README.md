# Agentic AI Workflows

This repository is a hands-on LangGraph learning project that combines notebook-based workflow experiments with a small Streamlit chatbot interface. It is designed for exploring agentic AI patterns, stateful orchestration, and structured LLM application flows in a simple, beginner-friendly setup.

## Project structure

- `Workflow/` — foundational LangGraph workflow examples
  - `bmi_workflow.ipynb` — deterministic BMI calculator workflow
  - `simple_llm_workflow.ipynb` — minimal LLM-driven workflow using LangGraph
- `conditional_workflow/` — branching and decision-based workflows
  - `quadratic_eq_conditnflow.ipynb` — quadratic equation solver with conditional logic
  - `Review_conditionalflow.ipynb` — supplementary conditional workflow review notebook
- `paralle_workflow/` — multi-task and parallel workflow examples
  - `cricket_workflow_paralle.ipynb` — parallel cricket analytics workflow
  - `UPSC_workflow_parallel.ipynb` — parallel essay evaluation workflow
- `Iterative_workflow/` — iterative generation workflows
  - `post_generation.ipynb` — multiple-step generation workflow example
- `chatBot/` — conversational bot experiments and persistence examples
  - `chatbot.ipynb` — chatbot workflow notebook
  - `persistence.ipynb` — state persistence example
  - `fault_tolerance.ipynb` — resilience-focused workflow notebook
- `chatbot_BE_FE/` — backend + frontend demo for a minimal chatbot app
  - `langgrapg_backned.py` — LangGraph backend graph definition
  - `streamlit_frontend.py` — Streamlit chat UI that talks to the backend
- `requirements.txt` — Python dependencies used across the project
- `env.example` — environment variable template
- `.env` — local environment file containing your API keys (not committed)

## Included workflow examples

### 1. Simple LLM workflow
`Workflow/simple_llm_workflow.ipynb` demonstrates a minimal LangGraph pipeline that:

- loads environment variables from `.env`
- connects to Groq using `ChatGroq`
- creates a stateful graph
- passes the user message through the model and returns a response

This is the best place to start if you are learning LangGraph basics.

### 2. BMI workflow
`Workflow/bmi_workflow.ipynb` shows a deterministic workflow that:

- accepts height and weight
- calculates BMI
- classifies the result into a health category
- moves through graph nodes in a fixed sequence

This helps explain typed state and sequential orchestration without needing external APIs.

### 3. Conditional workflow
`conditional_workflow/quadratic_eq_conditnflow.ipynb` explores branching logic in LangGraph by:

- taking coefficients `a`, `b`, and `c`
- calculating the discriminant
- determining whether a solution is real, repeated, or nonexistent
- routing execution through different graph paths based on the result

This is a practical introduction to conditional edges and graph-based decisions.

### 4. Parallel workflow examples
The notebooks in `paralle_workflow/` show how multiple tasks can execute within a shared graph:

- `cricket_workflow_paralle.ipynb` calculates batting metrics such as strike rate and boundary percentage
- `UPSC_workflow_parallel.ipynb` evaluates essay quality using structured reasoning and parallel scoring

These examples are useful when learning multi-step or parallel agent patterns.

### 5. Iterative workflow
`Iterative_workflow/post_generation.ipynb` illustrates iterative generation or follow-up workflow execution, helping show how an agent can build on earlier outputs over multiple stages.

### 6. Streamlit chatbot app
`chatbot_BE_FE/streamlit_frontend.py` and `chatbot_BE_FE/langgrapg_backned.py` provide a lightweight end-to-end chatbot example:

- the backend defines a LangGraph chatbot state and model invocation flow
- the frontend provides a Streamlit chat interface
- user messages are passed to the graph and displayed in the app UI

This is a good example of connecting a conversational AI backend to a simple web frontend.

## Prerequisites

- Python 3.10+
- Jupyter Notebook or VS Code with Python and Jupyter support
- Streamlit for the chatbot UI
- Internet access and a Groq API key for the LLM-powered examples

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install the project dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy the sample environment file:

   ```powershell
   Copy-Item env.example .env
   ```

4. Add your Groq API key to `.env`:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

   Do not commit `.env` or share your API key publicly.

## Running the notebooks

Open a notebook in Jupyter or VS Code and run the cells in order.

Typical notebook workflow:

```powershell
jupyter notebook
```

Then open the notebook you want to run in the browser or editor.

## Running the Streamlit chatbot

From the project root, start the app with:

```powershell
streamlit run chatbot_BE_FE\streamlit_frontend.py
```

If you are already inside the project folder, this is the simplest command:

```powershell
streamlit run .\chatbot_BE_FE\streamlit_frontend.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

This launches the chat UI and connects it to the LangGraph backend defined in `chatbot_BE_FE/langgrapg_backned.py`.

For a detailed walkthrough of the full execution flow, file connections, and how the frontend/backend interact, see [STREAMLIT_CHATBOT_FLOW.md](./STREAMLIT_CHATBOT_FLOW.md).

If Streamlit is not recognized, install it first:

```powershell
pip install streamlit
```

Then run the command again.

## Notes

- This repository is intended as a learning sandbox for agentic workflows and LangGraph experimentation.
- Some notebooks are deterministic and do not require external APIs.
- LLM-powered examples depend on Groq access and an active API key.

## License

This project is intended for educational and experimentation purposes.
