import os
import json
from datetime import datetime


TRAJECTORY_DIR = "sample_trajectories"


def save_trajectory(question, past_actions, context, final_answer, critique=None, evaluation=None):
    """
    Saves the full reasoning trajectory, including product search context if applicable.
    """
    trajectory = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "past_actions": past_actions,
        "context": context,
        "answer": final_answer,
        "critique": critique,
        "evaluation": evaluation,
        "notes": "For product-related tasks, ensure the trajectory captures if the agent followed these guidelines: "
                 "matched user goals, verified in-stock products with pricing and features, sourced from trusted sites, "
                 "and returned concise results."
    }

    os.makedirs(TRAJECTORY_DIR, exist_ok=True)
    filename = f"{TRAJECTORY_DIR}/trajectory_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(trajectory, file, ensure_ascii=False, indent=2)

    print(f"Trajectory saved to {filename}")
