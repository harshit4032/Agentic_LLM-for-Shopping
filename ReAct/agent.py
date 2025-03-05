# agent.py
import openai
import os
from tools import (calendar_tool, calculator_tool, wolfram_alpha_tool, machine_translation_tool, 
                   google_search_tool, wiki_search_tool, firecrawl_recommendation_tool)
from dotenv import load_dotenv

# === OpenAI Configuration ===
load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

# === MEMORY TOOL ===
memory = []  # Stores intermediate steps

# === LLM UTILITY ===
def gpt_call(prompt, model="gpt-3.5-turbo", temperature=0.5):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"].strip()

# === AGENT MODULES ===

def decision_step(question, context):
    prompt = f"""
Decide the next step to answer this question: "{question}".

Context so far:
{context}

Available tools:
1. Calendar
2. Calculator
3. Wolfram Alpha
4. Machine Translation
5. Google Search
6. Wikipedia Search
7. Firecrawl Product Recommendation
8. Recall Memory
9. Generate Answer
10. Terminate

What is your decision and why?
"""
    return gpt_call(prompt)

def tool_output_summarization(output):
    prompt = f"Summarize this tool output:\n{output}"
    return gpt_call(prompt)

def answer_generation(question, context):
    prompt = f"""
Using the context below, answer the question:

Question: {question}
Context: {context}
"""
    return gpt_call(prompt)

def relevance_self_check(answer, question):
    prompt = f"""
Evaluate if the answer is relevant.

Question: {question}
Answer: {answer}
"""
    return gpt_call(prompt)

def grounding_self_check(answer, context):
    prompt = f"""
Evaluate if the answer is grounded in the context.

Answer: {answer}
Context: {context}
"""
    return gpt_call(prompt)

# === MAIN AGENT CONTROLLER ===
def search_agent(question):
    context = ""
    for step in range(25):
        print(f"\n[Step {step + 1}] Decision Step:")
        decision = decision_step(question, context)
        print(decision)

        if "calendar" in decision.lower():
            result = calendar_tool(None)
        elif "calculator" in decision.lower():
            expression = gpt_call(f"Extract the math expression from: {question}")
            result = calculator_tool(expression)
        elif "wolfram alpha" in decision.lower():
            result = wolfram_alpha_tool(question)
        elif "machine translation" in decision.lower():
            result = machine_translation_tool(question)
        elif "google search" in decision.lower():
            result = google_search_tool(question)
        elif "wikipedia" in decision.lower():
            result = wiki_search_tool(question)
        elif "firecrawl" in decision.lower():
            result = firecrawl_recommendation_tool(question, question)
        # elif "recall memory" in decision.lower():
        #     result = recall_memory()
        elif "generate answer" in decision.lower():
            answer = answer_generation(question, context)
            relevance = relevance_self_check(answer, question)
            grounding = grounding_self_check(answer, context)
            return f"Answer: {answer}\nRelevance: {relevance}\nGrounding: {grounding}"
        elif "terminate" in decision.lower():
            return "Terminated early without answer."
        else:
            result = "[Unrecognized decision]"

        print(f"\n[Tool Output]: {result}")
        summary = tool_output_summarization(result)
        print(f"\n[Summarized Output]: {summary}")

        context += f"\n{summary}"
        memory.append(summary)

    return "Reached step limit without final answer."

# # === RUN AGENT ===
# if __name__ == "__main__":
#     question = "I need white sneakers (size 8) for under $70 that can arrive by Friday, give the link also"
#     final_response = search_agent(question)
#     print("\n=== Final Response ===")
#     print(final_response)
