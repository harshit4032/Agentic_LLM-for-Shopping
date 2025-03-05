from langgraph.store.memory import InMemoryStore
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchResults
import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict, Optional
import logging
import geocoder
from typing import Annotated
from typing_extensions import TypedDict
import os
## Working With Tools
from langgraph_supervisor import create_supervisor
from langgraph.graph import StateGraph,START,END
from langmem import create_multi_prompt_optimizer

from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import WikipediaAPIWrapper , DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper
from langchain_community.tools import WikipediaQueryRun , DuckDuckGoSearchResults
from tools import CurrentDateTimeTool, ShippingTimeEstimator, PromoCodeScraper , calculator , get_current_location , scrape_and_crawl
from langchain_core.tools import Tool
from langgraph.store.memory import InMemoryStore

from langgraph.prebuilt import create_react_agent
from langgraph.config import get_store

def prompt_search(state):
    item = store.get(("instructions",), key="search_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

def prompt_wiki(state):
    item = store.get(("instructions",), key="wiki_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

def prompt_promo_code(state):
    item = store.get(("instructions",), key="promo_code_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

def prompt_shipping(state):
    item = store.get(("instructions",), key="shipping_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

def prompt_calculator(state):
    item = store.get(("instructions",), key="calculator_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

def prompt_location(state):
    item = store.get(("instructions",), key="location_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

def prompt_scraper(state):
    item = store.get(("instructions",), key="scraper_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

def prompt_datetime(state):
    item = store.get(("instructions",), key="datetime_agent")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']

store = InMemoryStore()
store.put(("instructions",), key="agent_instructions", value={"prompt": "Help customer to find it's product and solve it's problem"})
search = GoogleSearchAPIWrapper()



Google_search = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)


api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=300)
wiki_tool=WikipediaQueryRun(api_wrapper=api_wrapper)

api_wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=2)
DuckDuckGo = DuckDuckGoSearchResults(api_wrapper=api_wrapper, source="news")


logger = logging.getLogger(__name__)

store = InMemoryStore()

tools=[wiki_tool,CurrentDateTimeTool,ShippingTimeEstimator,PromoCodeScraper,DuckDuckGo,Google_search,calculator,get_current_location,scrape_and_crawl]



store = InMemoryStore()

# Define tool instructions
store.put(("instructions",), key="search_agent", value={"prompt": "Search the web for relevant information."})
store.put(("instructions",), key="wiki_agent", value={"prompt": "Retrieve concise Wikipedia summaries."})
store.put(("instructions",), key="promo_code_agent", value={"prompt": "Find active promo codes for online stores."})
store.put(("instructions",), key="shipping_agent", value={"prompt": "Estimate shipping costs and delivery times."})
store.put(("instructions",), key="calculator_agent", value={"prompt": "Perform mathematical calculations."})
store.put(("instructions",), key="location_agent", value={"prompt": "Retrieve the user's current location."})
store.put(("instructions",), key="scraper_agent", value={"prompt": "Scrape and crawl web pages for data."})
store.put(("instructions",), key="datetime_agent", value={"prompt": "Retrieve the current date and time."})
# Initialize agents
search_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_search, tools=[GoogleSearchAPIWrapper], store=store, name="search_agent")
wiki_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_wiki, tools=[WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300))], store=store, name="wiki_agent")
promo_code_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_promo_code, tools=[PromoCodeScraper], store=store, name="promo_code_agent")
shipping_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_shipping, tools=[ShippingTimeEstimator], store=store, name="shipping_agent")
calculator_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_calculator, tools=[calculator], store=store, name="calculator_agent")
location_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_location, tools=[get_current_location], store=store, name="location_agent")
scraper_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_scraper, tools=[scrape_and_crawl], store=store, name="scraper_agent")
datetime_agent = create_react_agent("gpt-3.5-turbo", prompt=prompt_datetime, tools=[CurrentDateTimeTool], store=store, name="datetime_agent")


# Create supervisor workflow
workflow = create_supervisor(
    [search_agent, wiki_agent,promo_code_agent,shipping_agent,calculator_agent,location_agent,datetime_agent],
    model="gpt-3.5-turbo",
    prompt=(
        "You are a team supervisor managing multiple AI agents to assist with various tasks and a virtual shopping assistant that helps online shoppers navigate multiple fashion e-commerce platforms. You interpret user requests, decide which external tools to use, and integrate the obtained information to provide clear and helpful responses."
    )
)

workflow.add_edge('supervisor',END)
app = workflow.compile()
result = app.invoke(
    {"messages": [
        {"role": "user", "content": "hi"}
    ]}
)

feedback = {"request": "Always sign off from Shoppin Fashon AI; Enjoy Shopping see you soon!!"}

optimizer = create_multi_prompt_optimizer("gpt-3.5-turbo")

wiki_prompt = store.get(("instructions",), key="wiki_agent").value['prompt']
datetime_prompt = store.get(("instructions",), key="datetime_agent").value['prompt']
shipping_prompt = store.get(("instructions",), key="shipping_agent").value['prompt']
promo_prompt = store.get(("instructions",), key="promo_code_agent").value['prompt']
search_prompt = store.get(("instructions",), key="search_agent").value['prompt']
calculator_prompt = store.get(("instructions",), key="calculator_agent").value['prompt']
location_prompt = store.get(("instructions",), key="location_agent").value['prompt']
scraper_prompt = store.get(("instructions",), key="scraper_agent").value['prompt']

location_prompt = {
    "name": "location_prompt",
    "prompt": location_prompt,
    "when_to_update": "if unable to retrive the location take the capital of the cuntry."
}
wiki_prompt = {
    "name": "wiki_prompt",
    "prompt": wiki_prompt,
    "when_to_update": "Update if Wikipedia search results are inaccurate, outdated, or lack sufficient detail for user queries."
}

datetime_prompt = {
    "name": "datetime_prompt",
    "prompt": datetime_prompt,
    "when_to_update": "Update if the date/time format needs localization, time zones are incorrect, or response speed is slow."
}

shipping_prompt = {
    "name": "shipping_prompt",
    "prompt": shipping_prompt,
    "when_to_update": "Update if shipping cost or delivery time estimates are inaccurate, missing key carrier options, or not reflecting real-time data."
}

promo_prompt = {
    "name": "promo_prompt",
    "prompt": promo_prompt,
    "when_to_update": "Update if promo codes are expired, missing from key sources, or fail to provide valid discounts on supported platforms."
}


search_prompt = {
    "name": "search_prompt",
    "prompt": search_prompt,
    "when_to_update": "Update if search results are outdated, irrelevant, or fail to retrieve comprehensive information from authoritative sources."
}

calculator_prompt = {
    "name": "calculator_prompt",
    "prompt": calculator_prompt,
    "when_to_update": "Update if calculations are inaccurate, fail to support additional operations (e.g., percentages, advanced math), or execution speed is slow."
}

location_prompt = {
    "name": "location_prompt",
    "prompt": location_prompt,
    "when_to_update": "Update if location data is incorrect, fails to detect user’s region, or lacks sufficient details like city, state, or country."
}

scraper_prompt = {
    "name": "scrape_crawl_prompt",
    "prompt": scraper_prompt,
    "when_to_update": "Update if web scraping retrieves outdated, incomplete, or irrelevant data, or if crawling speed needs optimization for large-scale websites."
}

optimizer_result = optimizer.invoke({
    "prompts": [
        datetime_prompt, 
        shipping_prompt, 
        promo_prompt, 
        search_prompt,  
        calculator_prompt, 
        location_prompt, 
        scraper_prompt,
        location_prompt
    ],
    "trajectories": [(result["messages"], feedback)]
})


for i in range(len(optimizer_result)):
    store.put(("instructions",), key=optimizer_result[i]['name'], value={"prompt": optimizer_result[i]['prompt']})


prompt = input("Enter query: ")
result = app.invoke(
    {"messages": [
        {"role": "user", "content" :prompt}]},
)
result['messages'][-1].pretty_print()