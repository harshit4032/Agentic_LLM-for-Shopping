import streamlit as st
import json
from agent import run_agent


st.set_page_config(page_title="Webshop Reasoning Agent", layout="wide")

st.title("Webshop Reasoning Agent")
st.markdown("""
This is the Self-Improvement Multi-Step Reasoning LLM Agent.
Enter your shopping-related question below, and the agent will perform multi-step reasoning and tool usage to answer your query.
""")


def parse_final_answer(answer):
    """
    Parse the final answer if it is valid JSON.
    """
    try:
        products = json.loads(answer)
        return products
    except json.JSONDecodeError:
        return []


question = st.text_input(
    "Enter your question:",
    placeholder="Example: Find a floral skirt under $40 in size S. Is it in stock, and can I apply the discount code 'SAVE10'?",
)

if st.button("Run Agent"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.info("Processing your request. Please wait...")

        # Run the agent
        result = run_agent(question)
        final_answer = result["answer"]

        st.subheader("Final Answer")

        products = parse_final_answer(final_answer)
        if products:
            for idx, product in enumerate(products, start=1):
                st.markdown(f"""
**{idx}. {product.get('name', 'Unknown Product')}**  
Price: {product.get('price', 'N/A')}  
Stock Status: {product.get('stock_status', 'N/A')}  
Features: {product.get('features', 'N/A')}  
Link: {product.get('link', '[No link provided]')}  
---
                """)
        else:
            st.markdown(final_answer)

        st.subheader("Self-Critique")
        st.markdown(result["critique"])

        st.subheader("Auto-Evaluation")
        evaluation = result["evaluation"]
        if isinstance(evaluation, dict):
            st.markdown(f"- Correctness: {evaluation.get('correctness', 0)}")
            st.markdown(f"- Completeness: {evaluation.get('completeness', 0)}")
            st.markdown(f"- Relevance: {evaluation.get('relevance', 0)}")
            st.markdown(f"- Explanation: {evaluation.get('explanation', 'N/A')}")
        else:
            st.markdown(f"{evaluation}")

        st.subheader("Reasoning Trajectory")
        for i, action in enumerate(result["trajectory"], start=1):
            st.markdown(f"""
**Step {i}**
- Tool: `{action['action']}`
- Input: `{action['input']}`
- Output: `{action['output']}`
---
            """)
