### ✅ Here is the full `README.md` in markdown format:

---

```markdown
# WebShop Reasoning Agent

This project implements a **Self-Improvement Multi-Step Reasoning LLM Agent** designed to handle complex product search tasks using multi-step reasoning, dynamic tool use, adaptive reflection, and self-improvement inspired by **ReST meets ReAct** and **Chain of Tools** methodologies.

The agent supports:
- Multi-step reasoning over product queries.
- Real-time product search and comparison.
- Discount checking, shipping estimation, competitor price comparison, and return policy validation.
- Reflection, self-critique, auto-evaluation, and iterative self-improvement with fine-tuning.
- WebShop dataset evaluation and customization.

---

## Features

- Multi-tool support:
  - Google Search (via Custom Search API)
  - Wikipedia Search
  - Calendar, Calculator, WolframAlpha
  - Firecrawl for advanced web crawling
  - Discount checker, shipping estimator, return policy checker, competitor price comparison, and more
- Adaptive reflection and failure handling.
- Automatic self-critique and auto-evaluation.
- WebShop dataset integration.
- Fine-tuning and iterative self-improvement.
- Local interactive interface via **Streamlit**.

---

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/your-repo/webshop-reasoning-agent.git
cd webshop-reasoning-agent
```

### 2. Set up the environment:
```bash
conda env create -f environment.yml
conda activate llm_agent
```

### 3. Install required packages:
```bash
pip install -r requirements.txt
```

### 4. Configure API keys:
Create a `.env` file with your keys:
```env
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
WOLFRAM_ALPHA_APPID=your_wolframalpha_app_id
BING_API_KEY=your_bing_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

---

## Usage

### Run the full agent pipeline:
```bash
python main.py
```
This will:
- Run an example product reasoning task.
- Test predefined WebShop tasks (A–E).
- Build sample trajectories.
- Generate and upload a fine-tuning dataset.
- Start fine-tuning and generate reports.
- Visualize evaluation results.

### Run the local web app:
```bash
streamlit run app.py
```
Then open `http://localhost:8501/` in your browser.

---

## Example Query

```
Find a floral skirt under $40 in size S. Is it in stock, and can I apply the discount code 'SAVE10'?
```

The agent will:
1. Search for matching products.
2. Check stock status.
3. Apply discounts where possible.
4. Return top product recommendations in a structured format.

---

## Project Structure

```
├── agent.py
├── tools.py
├── memory.py
├── reflection.py
├── ranking.py
├── evaluation.py
├── webshop_loader.py
├── webshop_test_runs.py
├── webshop_sample_trajectories.py
├── fine_tuning_dataset_builder.py
├── fine_tuning_uploader.py
├── report_generator.py
├── visualize_results.py
├── prompts.py
├── app.py
├── main.py
├── requirements.txt
├── environment.yml
└── .env
```

---

## Datasets

- Integrated with the **WebShop dataset** for evaluation and self-improvement.
- Supports trajectory generation, fine-tuning dataset creation, and evaluation.

---

## Self-Improvement Workflow

- Reflection on tool failures.
- Adaptive retries, tool switching, and fallback strategies.
- Self-critique and guided improvements.
- Auto-evaluation based on correctness, completeness, and relevance.
- Iterative fine-tuning with collected trajectories.

---

## Credits

This project is inspired by:
- **ReST meets ReAct: Self-Improvement for Multi-Step Reasoning LLM Agent**.
- **Chain of Tools: Large Language Model is an Automatic Multi-tool Learner**.

---

## License

This project is licensed under the **MIT License**.
```

---

### ✅ Would you like me to:
- Save this as `README.md` into your project directly?
- Customize any sections (author, repository links, or examples)?