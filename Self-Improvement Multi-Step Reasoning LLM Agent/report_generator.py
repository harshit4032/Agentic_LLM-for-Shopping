import json
import pandas as pd


def load_results(results_file):
    """
    Loads evaluation results from a JSON file.
    """
    with open(results_file, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_report(results, output_file="evaluation_report.md"):
    """
    Generates a Markdown report from evaluation results.
    """
    def safe_evaluation(evaluation):
        if isinstance(evaluation, dict):
            return evaluation
        else:
            return {}

    processed_results = []
    for idx, r in enumerate(results):
        evaluation = safe_evaluation(r.get("evaluation"))
        processed_results.append({
            "task_id": r.get("task_id", f"task_{idx + 1}"),
            "goal": r.get("question", "N/A"),
            "answer": r.get("answer", "N/A"),
            "correctness": evaluation.get("correctness", 0),
            "completeness": evaluation.get("completeness", 0),
            "relevance": evaluation.get("relevance", 0),
            "explanation": evaluation.get("explanation", "")
        })

    df = pd.DataFrame(processed_results)
    avg_scores = df[["correctness", "completeness", "relevance"]].mean()

    with open(output_file, "w", encoding="utf-8") as report:
        report.write("# Webshop Agent Evaluation Report\n\n")
        report.write(f"### Average Scores:\n")
        report.write(f"- Correctness: {avg_scores['correctness']:.2f}\n")
        report.write(f"- Completeness: {avg_scores['completeness']:.2f}\n")
        report.write(f"- Relevance: {avg_scores['relevance']:.2f}\n\n")

        report.write(f"### Top 5 Tasks by Correctness:\n")
        for _, row in df.nlargest(5, "correctness").iterrows():
            report.write(format_task_summary(row))

        report.write(f"\n### Bottom 5 Tasks by Correctness:\n")
        for _, row in df.nsmallest(5, "correctness").iterrows():
            report.write(format_task_summary(row))

    print(f"Report generated at '{output_file}'")


def format_task_summary(row):
    return (
        f"\n#### Task {row['task_id']}\n"
        f"- Goal: {row['goal']}\n"
        f"- Answer: {row['answer']}\n"
        f"- Correctness: {row['correctness']}\n"
        f"- Completeness: {row['completeness']}\n"
        f"- Relevance: {row['relevance']}\n"
        f"- Explanation: {row['explanation']}\n"
    )
