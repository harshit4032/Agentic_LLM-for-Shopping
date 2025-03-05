from dotenv import load_dotenv
load_dotenv()
from typing import List, Optional
from pydantic import BaseModel, Field
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from tools import CurrentDateTimeTool, ShippingTimeEstimator, PromoCodeScraper , UserLocationTool
from phi.tools.firecrawl import FirecrawlTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch
from phi.tools.website import WebsiteTools
from phi.tools.calculator import Calculator
import json



#  Fix: Remove response_model & structured_outputs
reasoning_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="A shopping assistant that provides structured responses.",
    structured_outputs=True, 
    instructions=[
    # "You are a virtual shopping assistant for fashion e-commerce.",
    "Include product name, price, sizes, discounts, shipping, delivery, store, and purchase link.",
    "Provide accurate, relevant results with functional links.",
],
add_history_to_messages=True,
    tools=[
        FirecrawlTools(),
        DuckDuckGo(),
        GoogleSearch(),
        WebsiteTools(),
        CurrentDateTimeTool(),
        # PromoCodeScraper(),
        Calculator(add=True, subtract=True, multiply=True, divide=True),
        UserLocationTool()
    ],
    reasoning=True
)

#  Fetch shopping results and manually extract JSON
def get_shopping_recommendations(query: str):
    response = reasoning_agent.run(query)
    print("\nRaw Response:\n", response.content)

    # Extract JSON from Markdown code block
    try:
        start = response.content.find("{")
        end = response.content.rfind("}") + 1
        json_data = json.loads(response.content[start:end])
        print("\nParsed JSON Response:\n", json.dumps(json_data, indent=2))
    except Exception as e:
        print("\n Error parsing JSON:", e)

# Test function


import os
import json
from gorq_agent import  get_shopping_recommendations
from openai_agent import reasoning_agent

SAMPLE_TRAJECTORY_DIR = "sample_trajectories"
os.makedirs(SAMPLE_TRAJECTORY_DIR, exist_ok=True)


def save_sample_trajectory(agent_name,task_name, question,reasoning_agent):
    """
    Runs the agent on a question and saves the result as a trajectory.
    """

    # result = reasoning_agent.print_response(question, stream=True, show_full_reasoning=True)
    result = reasoning_agent.run(question)
    print(result.content)
    trajectory = {
        "agent_name": agent_name,
        "task_name": task_name,
        "question": question,
        "answer": result.content
    }

    filename = f"{SAMPLE_TRAJECTORY_DIR}/{task_name.replace(' ', '_').lower()}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(trajectory, file, indent=2, ensure_ascii=False)

    print(f"Saved trajectory: {filename}")


def build_sample_trajectories(agent_name,reasoning_agent):
    """
    Builds sample trajectories for Webshop tasks A–E.
    """
    tasks = [
        ("Task A", "Find a floral skirt under $40 in size S. Is it in stock, and can I apply a discount code 'SAVE10'?"),
        ("Task B", "I need white sneakers (size 8) for under $70 that can arrive by Friday."),
        ("Task C", "I found a 'casual denim jacket' at $80 on H&M. Any better deals?"),
        ("Task D", "I want to buy a cocktail dress from ZARA, but only if returns are hassle-free. Do they accept returns?"),
        ("Task E", "Find a waterproof hiking backpack under $100 with free shipping, check if I can use the code 'HIKER20', and compare prices across sites.")
    ]

    for task_name, question in tasks:
        save_sample_trajectory(agent_name,task_name, question,reasoning_agent)



build_sample_trajectories('OpenAI',reasoning_agent)
# prompt = input("Enter query: ")
# # get_shopping_recommendations(prompt)
# reasoning_agent.print_response(prompt, stream=True, show_full_reasoning=True)
