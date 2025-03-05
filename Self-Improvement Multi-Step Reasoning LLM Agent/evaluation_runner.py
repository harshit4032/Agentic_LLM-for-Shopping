import json
import os
from agent import run_agent
from webshop_loader import load_webshop_dataset


def evaluate_agent(output_file="evaluation_results/all_results.json"):
    """
    Runs evaluation on the full Webshop dataset and saves the results.
    """
    print("\nRunning evaluation on the Webshop dataset...")

    dataset = load_webshop_dataset()
    results = []

    for idx, example in enumerate(dataset):
        question = example["question"]
        print(f"\nEvaluating question: {question}")

        result = run_agent(question)

        results.append({
            "task_id": f"task_{idx + 1}",
            "question": question,
            "answer": result["answer"],
            "critique": result["critique"],
            "evaluation": result["evaluation"],
            "trajectory": result["trajectory"]
        })

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    print(f"\nEvaluation completed. Results saved to '{output_file}'.")
