import os
import json
import glob

SAMPLE_TRAJECTORY_DIR = "sample_trajectories"
FINE_TUNING_DATASET_FILE = "fine_tuning_dataset.jsonl"


def build_fine_tuning_dataset():
    """
    Converts sample trajectories into a JSONL fine-tuning dataset, handling missing fields.
    """
    dataset = []

    for filepath in glob.glob(f"{SAMPLE_TRAJECTORY_DIR}/*.json"):
        with open(filepath, "r", encoding="utf-8") as file:
            trajectory = json.load(file)

        question = trajectory.get("question", "No question provided.")
        answer = trajectory.get("answer", "No answer provided.")
        critique = trajectory.get("critique", "No critique available.")

        entry = {
            "prompt": f"Task: {question}\n\nCritique:\n{critique}\n\nGenerate the best answer.",
            "completion": answer
        }

        dataset.append(entry)

    with open(FINE_TUNING_DATASET_FILE, "w", encoding="utf-8") as out_file:
        for entry in dataset:
            out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Fine-tuning dataset saved to '{FINE_TUNING_DATASET_FILE}' with {len(dataset)} samples.")
