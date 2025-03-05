import os
import json
from Multitool_agent import  agent as MT_agent
from Multitooling_self_improvement_agent import agent as MTSI_agent

SAMPLE_TRAJECTORY_DIR = "sample_trajectories"
os.makedirs(SAMPLE_TRAJECTORY_DIR, exist_ok=True)


def save_sample_trajectory(agent_name,task_name, question):
    """
    Runs the agent on a question and saves the result as a trajectory.
    """
    if agent_name=='Multitooling_agent':
        result = MT_agent(question)
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

    else:
        for i in range(5):
            result = MTSI_agent(question)

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
    build_sample_trajectories('Multitooling_agent')
    build_sample_trajectories('Multitooling_self_improvement')

