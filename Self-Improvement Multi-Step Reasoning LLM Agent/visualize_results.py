import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


import pandas as pd


def create_score_dataframe(results):
    """
    Creates a pandas DataFrame from evaluation results with correctness, completeness, and relevance scores.
    """
    def safe_evaluation(evaluation):
        if isinstance(evaluation, dict):
            return evaluation
        else:
            return {}

    data = []
    for r in results:
        evaluation = safe_evaluation(r.get("evaluation"))
        data.append({
            "task_id": r.get("task_id", "unknown_task"),
            "goal": r.get("question", "N/A"),
            "answer": r.get("answer", "N/A"),
            "correctness": evaluation.get("correctness", 0),
            "completeness": evaluation.get("completeness", 0),
            "relevance": evaluation.get("relevance", 0),
            "explanation": evaluation.get("explanation", "")
        })
    return pd.DataFrame(data)


def summarize_results(df):
    """
    Prints the average scores from the evaluation DataFrame.
    """
    avg_scores = df[["correctness", "completeness", "relevance"]].mean()
    print("\n=== Average Scores ===")
    print(f"Correctness: {avg_scores['correctness']:.2f}")
    print(f"Completeness: {avg_scores['completeness']:.2f}")
    print(f"Relevance: {avg_scores['relevance']:.2f}")



def plot_scores(df):
    """
    Plots correctness, completeness, and relevance over tasks.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="task_id", y="correctness", label="Correctness", marker="o")
    sns.lineplot(data=df, x="task_id", y="completeness", label="Completeness", marker="o")
    sns.lineplot(data=df, x="task_id", y="relevance", label="Relevance", marker="o")
    plt.title("Agent Performance Across Webshop Tasks")
    plt.xlabel("Task ID")
    plt.ylabel("Score (0-10)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

