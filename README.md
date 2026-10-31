# Agentic AI Video

This project contains two Jupyter notebooks demonstrating simple workflows built with LangGraph:

- `simple_llm_workflow.ipynb` builds a question-and-answer workflow using a Groq-hosted chat model.
- `bmi_workflow.ipynb` demonstrates a BMI calculation and category-labeling workflow.

## Setup

1. Create and activate a Python virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install the project dependencies:

   ```powershell
   pip install -r requirements.txt
   pip install langchain-groq
   ```s

3. Configure the Groq API key for the LLM notebook. Copy the example file and add your key:

   ```powershell
   Copy-Item env.example .env
   ```

   Set `GROQ_API_KEY` in `.env`. Keep this file private and do not commit your API key.

4. Open either notebook in Jupyter or VS Code and run its cells. The LLM notebook loads `.env` to authenticate with Groq.
