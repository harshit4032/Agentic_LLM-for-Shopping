import logging
import os
from agent import run_agent
from webshop_test_runs import test_task_a, test_task_b, test_task_c, test_task_d, test_task_e
from webshop_sample_trajectories import build_sample_trajectories
from fine_tuning_dataset_builder import build_fine_tuning_dataset
from fine_tuning_uploader import upload_and_start_fine_tuning
from evaluation_runner import evaluate_agent
from report_generator import load_results, generate_report
from visualize_results import create_score_dataframe, plot_scores, summarize_results
from config import EVALUATION_RESULTS_FILE, LOG_FILE


# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


if __name__ == "__main__":
    print("\nRunning Self-Improvement Multi-Step Reasoning LLM Agent\n")

    # Example: Run a single ad-hoc question
    question = "Find a floral skirt under $40 in size S. Is it in stock, and can I apply the discount code 'SAVE10'?"
    result = run_agent(question)

    print("\n=== Final Answer ===")
    print(result["answer"])

    print("\n=== Self-Critique ===")
    print(result["critique"])

    print("\n=== Auto-Evaluation ===")
    print(result["evaluation"])

    print("\n=== Trajectory ===")
    for step in result["trajectory"]:
        print(step)

    # Run Webshop test tasks
    test_task_a()
    test_task_b()
    test_task_c()
    test_task_d()
    test_task_e()

    # Build and save sample trajectories from Webshop tasks
    build_sample_trajectories()

    # Generate fine-tuning dataset from trajectories
    build_fine_tuning_dataset()

    # Upload dataset and start fine-tuning
    # upload_and_start_fine_tuning()

    # Run evaluation after fine-tuning and save the results
    evaluate_agent(output_file=EVALUATION_RESULTS_FILE)

    # Generate evaluation report and visualization if results exist
    if os.path.exists(EVALUATION_RESULTS_FILE):
        results = load_results(EVALUATION_RESULTS_FILE)
        generate_report(results)
        df = create_score_dataframe(results)
        summarize_results(df)
        plot_scores(df)
    else:
        print(f"\nEvaluation results file '{EVALUATION_RESULTS_FILE}' not found. Skipping report and visualization.")

    print("\nPipeline completed successfully.")
