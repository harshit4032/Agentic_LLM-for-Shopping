from gpt import gpt_call


AUTO_EVALUATION_PROMPT_TEMPLATE = """
# Auto-Evaluation

# Question:
"{question}"

# Final Answer:
\"\"\"{answer}\"\"\"

# Product Search Guidelines (if applicable):
When evaluating answers involving product searches:
- Confirm the answer matches the user's goal and context.
- Ensure product details are accurate, including name, price, features, and availability.
- Verify data sources are trusted e-commerce platforms like Google Shopping, Amazon, and Walmart.
- Check that the answer is concise and includes no more than 5 relevant products.

# Evaluation Task:
Evaluate the answer according to these criteria:
- Correctness (0-10)
- Completeness (0-10)
- Relevance (0-10)

Provide brief justifications for each score.

Return your evaluation as a JSON object:
{{
    "correctness": <score>,
    "completeness": <score>,
    "relevance": <score>,
    "explanation": "<brief explanation>"
}}
"""


SELF_CRITIQUE_PROMPT_TEMPLATE = """
# Self-Critique

# Question:
"{question}"

# Generated Answer:
\"\"\"{answer}\"\"\"

# Product Search Guidelines (if applicable):
When critiquing answers involving product searches:
- Check whether the user's goal was met.
- Identify any missing or incorrect product details.
- Suggest improvements to make the answer more accurate, complete, and relevant.

# Critique Task:
Analyze the answer and suggest improvements.
Return the critique as text.
"""


def auto_evaluate(question, answer):
    """
    Uses the LLM to automatically evaluate the final answer.
    """
    prompt = AUTO_EVALUATION_PROMPT_TEMPLATE.format(question=question, answer=answer)
    return gpt_call(prompt)


def self_critique(question, answer):
    """
    Uses the LLM to critique the final answer and suggest improvements.
    """
    prompt = SELF_CRITIQUE_PROMPT_TEMPLATE.format(question=question, answer=answer)
    return gpt_call(prompt)
