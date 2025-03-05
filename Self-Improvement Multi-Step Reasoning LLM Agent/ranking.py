import logging
from gpt import gpt_call


def rank_candidates(step_number, question, context, candidates):
    """
    Uses the LLM to rank multiple candidate outputs for a given reasoning step,
    applying product search guidelines when relevant.
    """
    formatted_candidates = "\n".join([f"{i + 1}. {c}" for i, c in enumerate(candidates)])

    prompt = f"""
# Reward Model Ranking

# Step Number:
{step_number}

# Question:
"{question}"

# Context:
\"\"\"{context}\"\"\"

# Candidate Outputs:
{formatted_candidates}

# Product Search Guidelines (if applicable):
When ranking candidates involving product search:
- Prefer actions that best match the user's goal and context.
- Prioritize candidates that use tools providing in-stock products with clear pricing and features.
- Favor data from trusted e-commerce sites like Google Shopping, Amazon, and Walmart.
- Select candidates that generate concise, top-5 product summaries.

# Task:
Rank the candidates from best to worst based on correctness, relevance, and usefulness.
Return the ranked list of indices (starting from 1).

ranking = [<indices in order>]
"""
    ranking_output = gpt_call(prompt)

    try:
        ranking = eval(ranking_output.split("ranking =")[1].strip())
        ranking = [int(i) - 1 for i in ranking]  # Convert to 0-based indices
    except Exception as e:
        logging.error(f"Failed to parse ranking output: {e}")
        ranking = list(range(len(candidates)))  # Default ranking if parsing fails

    logging.info(f"Ranking: {ranking}")
    return ranking
