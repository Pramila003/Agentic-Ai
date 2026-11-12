#!/usr/bin/env python
# coding: utf-8

# In[3]:


from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
from pathlib import Path
from dotenv import dotenv_values
from langsmith import traceable

# env_path = Path(r"D:\projects\Agentic Ai video\.env")

# config = dotenv_values(env_path)

# print("File exists:", env_path.exists())
# print("Available variables:", list(config.keys()))
# print("API key loaded:", bool(config.get("LANGSMITH_API_KEY")))


# In[21]:


class BatsmanState(TypedDict):
    runs:int
    balls:int
    fours:int
    sixes:int
    
    strikeRate:float
    boundryPerBall:float
    boundryPercentage:float
    summary:str


# In[22]:

@traceable(name="calculate_strikeRate")
def calculate_strikeRate(state:BatsmanState)-> BatsmanState:
    strikeRate= (state['runs']/state['balls'])* 100
    
    return {'strikeRate':strikeRate}


# In[23]:


def calculate_bpb(state: BatsmanState)->BatsmanState:
    boundryPerBall= state['balls']/(state['fours']+state['sixes'])
    
    return {'boundryPerBall':boundryPerBall}
    


# In[24]:


def calculate_boundry_percentage(state:BatsmanState)->BatsmanState:
    boundryPercentage= ((state['fours']*4 + state['sixes']*6)/state['runs'])*100

    return {'boundryPercentage':boundryPercentage}
    


# In[40]:


def summary(state:BatsmanState)->BatsmanState:
    summary_ret = f"""Batsman Summary:
    Runs: {state['runs']}
    Balls: {state['balls']}
    Fours: {state['fours']}
    Sixes: {state['sixes']}
    Strike Rate: {state['strikeRate']}
    Boundaries per Ball: {state['boundryPerBall']}
    Boundary Percentage: {state['boundryPercentage']}
    """
    
    return {'summary':summary_ret}


# In[41]:


graph =StateGraph(BatsmanState)
graph.add_node("calculate_strikeRate", calculate_strikeRate)
graph.add_node("calculate_bpb", calculate_bpb)
graph.add_node("calculate_boundary_percentage", calculate_boundry_percentage)
graph.add_node("summary",summary)

graph.add_edge(START, "calculate_strikeRate")
graph.add_edge(START, "calculate_bpb")
graph.add_edge(START, "calculate_boundary_percentage")

graph.add_edge("calculate_strikeRate", "summary")
graph.add_edge("calculate_bpb", "summary")
graph.add_edge("calculate_boundary_percentage", "summary")

graph.add_edge("summary", END)

workflow= graph.compile()


# In[42]:


from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())


# In[43]:


workflow


# In[44]:


initial_state={"runs":100,"balls":50,"fours":6,"sixes":4}
final_state=workflow.invoke(initial_state)
print(final_state)


# In[ ]:




