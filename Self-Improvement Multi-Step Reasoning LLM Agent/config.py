from dotenv import load_dotenv
load_dotenv()
import os
# === OpenAI Configuration ===
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if OPENAI_API_KEY:
    print("API Key loaded successfully!")
else:
    print("Failed to load API Key.")

# Fine-tuned model (replace with your model's ID after fine-tuning)

FINE_TUNED_MODEL = "gpt-3.5-turbo"

# Dataset Paths
TRAJECTORY_DIR = "sample_trajectories"
FINE_TUNING_DATASET_FILE = "fine_tuning_dataset.jsonl"
EVALUATION_RESULTS_FILE = "evaluation_results/all_results.json"
WEBHOP_TASKS_FILE = "webshop/tasks.jsonl"
WEBHOP_PRODUCTS_FILE = "webshop/products.jsonl"

# Logging
LOG_FILE = "agent_run.log"

# Agent Settings
MAX_STEPS = 10
MAX_SEARCHES = 10
DECISION_SAMPLE_SIZE = 4

# Evaluation Settings
NUM_EVAL_TASKS = 100
PRODUCTS_PER_TASK = 5