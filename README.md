# Agentic AI Workflows

This repository contains a set of small LangGraph-based notebooks that demonstrate agentic AI patterns, workflow orchestration, and structured LLM outputs. Each notebook focuses on a different use case and can be opened and run independently in VS Code or Jupyter.

## Project structure

- `simple_llm_workflow.ipynb` — basic LLM-driven workflow using Groq
- `bmi_workflow.ipynb` — deterministic workflow that calculates BMI and assigns a category
- `quadratic_eq_conditnflow.ipynb` — conditional workflow that evaluates a quadratic equation and routes based on the discriminant
- `cricket_workflow_paralle.ipynb` — cricket analytics workflow that computes batting metrics in a state-based graph
- `UPSC_workflow_parallel.ipynb` — a parallel evaluation workflow for grading UPSC-style essays using structured model output
- `requirements.txt` — Python dependencies needed for the notebooks
- `env.example` — sample environment file for the Groq API key
- `.env` — local environment file created by the user to store `GROQ_API_KEY` (not committed)

## Included workflows

### 1. Simple LLM workflow
`simple_llm_workflow.ipynb` demonstrates a lightweight LangGraph application that:

- loads environment variables from `.env`
- connects to Groq using `ChatGroq`
- creates a state graph
- passes user input through a language model and returns a result

This is the easiest example to start with when learning LangGraph and LLM integration.

### 2. BMI workflow
`bmi_workflow.ipynb` shows a simple workflow built around a typed state:

- accepts weight and height
- calculates BMI
- classifies the result as underweight, normal, overweight, or obese
- uses a graph structure to move from one computation step to the next

This is a clear example of state-driven orchestration without any external API dependency.

### 3. Quadratic equation workflow
`quadratic_eq_conditnflow.ipynb` demonstrates conditional branching in LangGraph for solving quadratic equations:

- accepts coefficients `a`, `b`, and `c`
- calculates the discriminant
- decides whether the equation has real roots, repeated roots, or no real roots
- routes execution through different graph nodes based on the computed result

This workflow is a good introduction to conditional graph edges and state-based decision logic.

### 4. Cricket workflow
`cricket_workflow_paralle.ipynb` explores cricket match analytics using a parallel state graph:

- reads batting inputs such as runs, balls, fours, and sixes
- calculates strike rate
- computes boundary per ball and boundary percentage
- produces a summary of the batting performance

This workflow is useful for understanding how multiple calculations can run as separate nodes in one graph.

### 5. UPSC essay evaluation workflow
`UPSC_workflow_parallel.ipynb` is a more advanced workflow that uses structured outputs for evaluation:

- loads an LLM model through Groq
- defines a schema for essay feedback and score
- evaluates an essay for strengths, weaknesses, and a numeric score
- uses LangGraph states to orchestrate a structured evaluation pipeline

This notebook is best for users exploring agentic evaluation systems and model-based scoring.

## Prerequisites

- Python 3.10+
- Jupyter Notebook or VS Code with Python/Jupyter extension
- Access to a Groq API key for the LLM-based notebooks

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

   If a notebook requires Groq and it is not already installed, install it separately:

   ```powershell
   pip install langchain-groq
   ```

3. Create your environment file:

   ```powershell
   Copy-Item env.example .env
   ```

4. Add your Groq API key to `.env`:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

   Never commit the `.env` file or share your API key publicly.

## Running the notebooks

Open any notebook in Jupyter or VS Code and run the cells in order.

Typical flow:

```powershell
jupyter notebook
```

Then select the notebook you want to run from the Jupyter interface.

## Notes

- The notebooks are designed as learning examples and demonstration workflows.
- Not all notebooks require API access; the BMI, cricket, and quadratic examples work as pure Python/LangGraph workflows.
- The LLM-based workflows depend on Groq credentials and internet connectivity.

## License

This project is intended for educational and experimentation purposes.
