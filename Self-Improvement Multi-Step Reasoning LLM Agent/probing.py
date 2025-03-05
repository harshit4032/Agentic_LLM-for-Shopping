import logging
from gpt import gpt_call


def probe_tool(tool_name):
    """
    Probes an unknown tool to infer its behavior.
    """
    # Generate a sample input for the tool
    probe_input = gpt_call(f"""
# Probe Input Generator

# Tool Name:
"{tool_name}"

# Task:
Generate an example input to test the tool.
probe_input = "<sample input>"
""")

    # Simulate probing output
    simulated_output = f"Simulated output of '{tool_name}' with input '{probe_input}'."

    # Summarize the behavior based on the probe
    behavior_summary = gpt_call(f"""
# Tool Behavior Summary

# Tool:
"{tool_name}"

# Probe Input:
"{probe_input}"

# Probe Output:
"{simulated_output}"

# Task:
Describe what this tool appears to do.
behavior_summary = "<summary of tool behavior>"
""")

    logging.info(f"Probed '{tool_name}': {behavior_summary}")
    return behavior_summary