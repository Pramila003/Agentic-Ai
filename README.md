# Agentic AI Workflows

This repository contains a collection of small LangGraph notebooks that demonstrate agentic AI patterns, state-based orchestration, and structured LLM workflows. The examples are designed for learning and experimentation in VS Code or Jupyter Notebook.

## Project structure

- `Workflow/` — basic workflow examples
  - `bmi_workflow.ipynb` — deterministic BMI calculator workflow
  - `simple_llm_workflow.ipynb` — simple LLM-driven LangGraph example
- `conditional_workflow/` — conditional branching examples
  - `quadratic_eq_conditnflow.ipynb` — quadratic equation solver with branching logic
  - `Review_conditionalflow.ipynb` — review/extension notebook for conditional flow patterns
- `paralle_workflow/` — parallel and structured-evaluation examples
  - `cricket_workflow_paralle.ipynb` — parallel cricket analytics workflow
  - `UPSC_workflow_parallel.ipynb` — parallel essay evaluation workflow
- `Iterative_workflow/` — iterative workflow example
  - `post_generation.ipynb` — notebook for iterative generation-style tasks
- `requirements.txt` — Python dependencies for the notebooks
- `env.example` — template for local environment variables
- `.env` — local environment file containing your API key (not committed)

## Included workflow examples

### 1. Simple LLM workflow
The `Workflow/simple_llm_workflow.ipynb` notebook shows a minimal LangGraph pipeline that:

- loads environment variables from `.env`
- connects to Groq through `ChatGroq`
- creates a stateful graph
- passes user input through the model and returns a result

This is the best place to start if you are learning LangGraph basics.

### 2. BMI workflow
The `Workflow/bmi_workflow.ipynb` notebook demonstrates a deterministic workflow that:

- accepts height and weight
- calculates BMI
- classifies the result into a health category
- moves through graph nodes in a structured sequence

This example is useful for understanding typed state and sequential orchestration without external APIs.

### 3. Conditional workflow
The `conditional_workflow/quadratic_eq_conditnflow.ipynb` notebook explores branching logic in LangGraph by:

- taking coefficients `a`, `b`, and `c`
- calculating the discriminant
- determining whether a solution is real, repeated, or nonexistent
- routing execution through different graph paths based on the result

This is a practical introduction to conditional edges and graph-based decision logic.

### 4. Parallel workflow examples
The notebooks in `paralle_workflow/` show how separate tasks can run within a common graph:

- `cricket_workflow_paralle.ipynb` calculates batting metrics such as strike rate and boundary percentage
- `UPSC_workflow_parallel.ipynb` evaluates essay quality using structured model output and parallel scoring logic

These examples are useful when learning multi-step or parallel agent patterns.

### 5. Iterative workflow
The `Iterative_workflow/post_generation.ipynb` notebook provides an example of iterative generation or follow-up workflow execution, helping illustrate how an agent can build on prior outputs in multiple stages.

## Prerequisites

- Python 3.10+
- Jupyter Notebook or VS Code with Python and Jupyter support
- Internet access and a Groq API key for the LLM-based notebooks

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

   If you plan to run the Groq-based notebooks, install the Groq integration package as well:

   ```powershell
   pip install langchain-groq
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

Typical workflow:

```powershell
jupyter notebook
```

Then open the notebook you want to run in the browser or editor.

## Notes

- The repository is intended as a learning sandbox for agentic workflows.
- Some notebooks are deterministic and do not require external APIs.
- The LLM-powered examples depend on Groq access and an active API key.

## License

This project is intended for educational and experimentation purposes.
