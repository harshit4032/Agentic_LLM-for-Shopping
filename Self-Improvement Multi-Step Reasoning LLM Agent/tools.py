import os
import requests
import calendar
import datetime
import wolframalpha
import wikipedia
from dotenv import load_dotenv
from operator import pow, truediv, mul, add, sub
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from googleapiclient.discovery import build
from phi.agent import Agent
from phi.tools.firecrawl import FirecrawlTools
from phi.model.groq import Groq

load_dotenv()


# Calendar Tool
def calendar_tool(_):
    now = datetime.datetime.now()
    return f"Today is {calendar.day_name[now.weekday()]}, {calendar.month_name[now.month]} {now.day}, {now.year}."


# Calculator Tool
def calculator_tool(expression):
    operators = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv
    }
    if expression.isdigit():
        return float(expression)
    for c in operators:
        left, operator, right = expression.partition(c)
        if operator in operators:
            return round(operators[operator](calculator_tool(left), calculator_tool(right)), 2)
    return "Invalid expression."


# Wolfram Alpha Calculator
def wolfram_alpha_tool(query):
    wolfram_alpha_appid = os.environ.get('WOLFRAM_ALPHA_APPID')
    client = wolframalpha.Client(wolfram_alpha_appid)
    res = client.query(query)
    assumption = next(res.pods).text
    answer = next(res.results).text
    return f"Assumption: {assumption}\nAnswer: {answer}"


# Machine Translation Tool
def machine_translation_tool(query, model_name="facebook/nllb-200-distilled-600M", target_lang="eng_Latn"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    input_ids = tokenizer(query, return_tensors="pt")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(f"<{target_lang}>")
    outputs = model.generate(**input_ids, forced_bos_token_id=forced_bos_token_id)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]


# Google Custom Search Tool
def google_search_tool(query, num_results=5):
    api_key = os.environ.get('GOOGLE_API_KEY')
    cse_id = os.environ.get('GOOGLE_CSE_ID')
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
    items = res.get("items", [])
    results = [f"{item['title']}: {item['link']}" for item in items]
    return "\n".join(results) if results else "No results found."


# Wikipedia Summary Search Tool
def wiki_search_tool(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return f"Wikipedia search error: {str(e)}"


# Firecrawl Product Recommendation Tool
def firecrawl_recommendation_tool(tool_input, question):
    agent = Agent(
        name="Web Product Crawler",
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        instructions=[
            "Act as a product search agent for e-commerce tasks.",
            "Find products matching the user's goal based on provided context.",
            "Prioritize accurate, in-stock items with clear pricing and features.",
            "Gather data from reliable sources like Google Shopping, Amazon, and Walmart.",
            "Return the top 5 results with name, price, features, availability, and link.",
            "Format responses clearly and concisely."
        ]
        ,
        tools=[FirecrawlTools()],
        markdown=True
    )

    query = f"""
    User's goal: {question}
    Product focus: {tool_input}
    Please search and return the top 5 most relevant products.
    """

    try:
        output = agent.run(query)
        return output.content
    except Exception as e:
        return f"Firecrawl error: {str(e)}"


# Tool Registry
TOOLS = {
    "calendar": calendar_tool,
    "calculator": calculator_tool,
    "wolfram_alpha": wolfram_alpha_tool,
    "machine_translation": machine_translation_tool,
    "google_search": google_search_tool,
    "wiki_search": wiki_search_tool,
    "firecrawl_recommendation": firecrawl_recommendation_tool
}
