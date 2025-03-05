# Product Search Guidance
PRODUCT_SEARCH_GUIDANCE = """
For product-related tasks:
- Match the user's goal and context.
- Prioritize in-stock items with clear pricing and feature details.
- Use trusted sources like Google Shopping, Amazon, and Walmart.
- Return up to 5 concise results with name, price, features, stock status, and link.
"""

# Decision step prompt template
DECISION_PROMPT_TEMPLATE = """
# Python code for Search Agent Decision Step

# Question:
question = "{question}"

# Past Actions:
past_actions = \"\"\"{past_actions}\"\"\"

# Available Tools:
tools = [
    "web_search",
    "date_time",
    "calculator",
    "wikipedia",
    "recall_memory",
    "product_page_reader",
    "search_aggregator",
    "discount_checker",
    "shipping_estimator",
    "competitor_price_comparison",
    "return_policy_checker",
    "firecrawl_recommendation",
    "generate_answer",
    "terminate"
]

# Remaining Searches:
remaining_searches = {remaining_searches}

# Guidelines:
{PRODUCT_SEARCH_GUIDANCE}

# Next Step:
# Decide the next action as Python code:
next_step = {{
    "action": "<tool_name>",
    "input": "<tool_input>",
    "reason": "<explanation of why this tool and input are needed>"
}}
"""

# Answer generation prompt template
ANSWER_GENERATION_PROMPT_TEMPLATE = """
# Python code for Search Agent Answer Generation Step

# Question:
question = "{question}"

# Context from Previous Steps:
context = \"\"\"{context}\"\"\"

# Guidelines:
{PRODUCT_SEARCH_GUIDANCE}

# Generate the final answer:
final_answer = \"\"\"<insert final answer here>\"\"\"
"""

# Self-critique prompt template
SELF_CRITIQUE_PROMPT_TEMPLATE = """
# Python code for Search Agent Self-Critique Step

# Question:
question = "{question}"

# Generated Answer:
answer = \"\"\"{answer}\"\"\"

# Guidelines:
{PRODUCT_SEARCH_GUIDANCE}

# Critique the answer and suggest improvements:
critique = \"\"\"<insert critique here>\"\"\"
"""
ANSWER_GENERATION_PROMPT_TEMPLATE = """
# Python code for Search Agent Answer Generation Step

# Question:
question = "{question}"

# Context from Previous Steps:
context = \"\"\"{context}\"\"\"

# Guidelines:
- Match the user's goal and context.
- Prioritize in-stock products with clear price and feature details.
- Use trusted sources like Google Shopping, Amazon, and Walmart.
- Return up to 5 relevant products.
- Ensure all products meet the user’s criteria.
- Output the final answer strictly as JSON, with this format:

[
  {{
    "name": "Product Name",
    "price": "$Price",
    "stock_status": "In Stock / Out of Stock",
    "features": "Key features of the product",
    "link": "Product URL"
  }},
  ...
]

# Generate the final_answer as JSON below:
final_answer =
"""
