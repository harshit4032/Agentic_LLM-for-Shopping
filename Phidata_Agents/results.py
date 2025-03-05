import os
import json
from gorq_agent import  get_shopping_recommendations
from openai_agent import reasoning_agent

SAMPLE_TRAJECTORY_DIR = "sample_trajectories"
os.makedirs(SAMPLE_TRAJECTORY_DIR, exist_ok=True)


def save_sample_trajectory(agent_name,task_name, question):
    """
    Runs the agent on a question and saves the result as a trajectory.
    """
    if agent_name=='OpenAI':
        result = reasoning_agent.print_response(question, stream=True, show_full_reasoning=True)
    else:
        result = get_shopping_recommendations(question)

    trajectory = {
        "agent_name": agent_name,
        "task_name": task_name,
        "question": question,
        "answer": result
    }

    filename = f"{SAMPLE_TRAJECTORY_DIR}/{task_name.replace(' ', '_').lower()}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(trajectory, file, indent=2, ensure_ascii=False)

    print(f"Saved trajectory: {filename}")


def build_sample_trajectories(agent_name):
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
        save_sample_trajectory(agent_name,task_name, question)

if __name__ == "__main__":
    build_sample_trajectories('llama3-70b-8192')
    build_sample_trajectories('OpenAI')

