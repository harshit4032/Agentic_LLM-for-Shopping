import logging
from prompts import (
    DECISION_PROMPT_TEMPLATE,
    ANSWER_GENERATION_PROMPT_TEMPLATE,
    SELF_CRITIQUE_PROMPT_TEMPLATE,
    PRODUCT_SEARCH_GUIDANCE,
)
from tools import TOOLS
from memory import Memory
from reflection import reflect_on_failure
from ranking import rank_candidates
from evaluation import auto_evaluate, self_critique
from gpt import gpt_call  # Added to execute prompts

memory = Memory()


def format_past_actions(past_actions):
    return "\n".join(
        f"Step {i + 1}: Tool = {action['action']}, Input = {action['input']}, Output = {action['output']}"
        for i, action in enumerate(past_actions)
    )


def sample_decisions(question, past_actions, remaining_searches):
    prompt = DECISION_PROMPT_TEMPLATE.format(
        question=question,
        past_actions=format_past_actions(past_actions),
        remaining_searches=remaining_searches,
        PRODUCT_SEARCH_GUIDANCE=PRODUCT_SEARCH_GUIDANCE
    )
    decisions = gpt_call(prompt)
    return [decisions]


def generate_final_answer(question, context):
    prompt = ANSWER_GENERATION_PROMPT_TEMPLATE.format(
        question=question,
        context=context,
        PRODUCT_SEARCH_GUIDANCE=PRODUCT_SEARCH_GUIDANCE
    )
    return gpt_call(prompt)


def critique_answer(question, answer):
    prompt = SELF_CRITIQUE_PROMPT_TEMPLATE.format(
        question=question,
        answer=answer,
        PRODUCT_SEARCH_GUIDANCE=PRODUCT_SEARCH_GUIDANCE
    )
    return gpt_call(prompt)


def run_agent(question):
    logging.info(f"Running Self-Improvement Multi-Step Reasoning LLM Agent")
    memory.add(f"Question: {question}")

    past_actions = []
    remaining_searches = 10
    max_steps = 20

    for step in range(max_steps):
        print(f"\nStep {step + 1}")
        decision_candidates = sample_decisions(question, past_actions, remaining_searches)
        ranked_indices = rank_candidates(step + 1, question, format_past_actions(past_actions), decision_candidates)
        best_decision = decision_candidates[ranked_indices[0]]

        action = eval(best_decision.split("next_step =")[1].strip())
        tool_name = action["action"]
        tool_input = action["input"]

        if tool_name == "terminate":
            print("Terminating.")
            break

        tool = TOOLS.get(tool_name)
        if not tool:
            print(f"Unknown tool: {tool_name}")
            break

        try:
            if isinstance(tool_input, dict):
                tool_output = tool(**tool_input, question=question)
            else:
                tool_output = tool(tool_input, question) if "question" in tool.__code__.co_varnames else tool(tool_input)
        except Exception as e:
            tool_output = f"Error: {e}"

        print(f"{tool_name} output: {tool_output}")

        past_actions.append({
            "action": tool_name,
            "input": tool_input,
            "output": tool_output
        })

        memory.add(f"Step {step + 1}: {tool_name} => {tool_output}")

        if tool_name == "generate_answer":
            break

        if tool_output.startswith("Error"):
            reflection = reflect_on_failure(step + 1, tool_name, tool_input, tool_output, format_past_actions(past_actions))
            if reflection["action"] == "retry":
                continue
            elif reflection["action"] == "replace_tool":
                tool_name = reflection["fix"]
                continue
            elif reflection["action"] == "skip":
                continue

        remaining_searches -= 1
        if remaining_searches <= 0:
            print("Reached search limit.")
            break

    context = format_past_actions(past_actions)
    final_answer = generate_final_answer(question, context)
    print("\n=== Final Answer ===")
    print(final_answer)

    critique = critique_answer(question, final_answer)
    print("\n=== Self-Critique ===")
    print(critique)

    evaluation = auto_evaluate(question, final_answer)
    print("\n=== Evaluation ===")
    print(evaluation)

    return {
        "answer": final_answer,
        "critique": critique,
        "evaluation": evaluation,
        "trajectory": past_actions
    }
