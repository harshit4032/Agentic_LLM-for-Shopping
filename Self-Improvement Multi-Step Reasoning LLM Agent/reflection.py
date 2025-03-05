import re
import logging
from gpt import gpt_call


def reflect_on_failure(step_number, tool_name, tool_input, tool_output, context):
    """
    Uses the LLM to analyze a failed tool output and suggest a correction,
    applying product search guidelines when relevant.
    """
    prompt = f"""
# Reflection on Tool Failure

# Step Number:
{step_number}

# Tool:
"{tool_name}"

# Input:
"{tool_input}"

# Output:
"{tool_output}"

# Context:
\"\"\"{context}\"\"\"

# Product Search Guidelines (if applicable):
When reflecting on product search failures:
- Ensure the tool attempted to match the user's goal.
- Verify products were in stock with clear pricing and feature details.
- Check that data was sourced from trusted e-commerce sites like Google Shopping, Amazon, and Walmart.
- Confirm that no more than 5 concise and relevant products were returned.

# Task:
Identify the problem and suggest one of the following actions:
- retry (with corrected input)
- replace_tool (with an alternative tool name)
- skip (if no correction is possible)

Provide:
- fix: Suggested fix or alternative tool
- action: retry | replace_tool | skip
- reason: Explanation for the decision

reflection = {{
    "fix": "<suggested fix or replacement>",
    "action": "<retry|replace_tool|skip>",
    "reason": "<reason>"
}}
"""
    reflection_output = gpt_call(prompt)

    fix = re.search(r"fix\s*:\s*(.*)", reflection_output, re.IGNORECASE)
    action = re.search(r"action\s*:\s*(.*)", reflection_output, re.IGNORECASE)
    reason = re.search(r"reason\s*:\s*(.*)", reflection_output, re.IGNORECASE)

    reflection_result = {
        "fix": fix.group(1).strip() if fix else None,
        "action": action.group(1).strip().lower() if action else "skip",
        "reason": reason.group(1).strip() if reason else "No reason provided."
    }

    logging.info(f"Reflection: {reflection_result}")
    return reflection_result
