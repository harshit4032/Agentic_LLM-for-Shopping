from typing import Annotated
from typing_extensions import TypedDict
import os

from langgraph.store.memory import InMemoryStore
## Working With Tools

from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import WikipediaAPIWrapper , DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper
from langchain_community.tools import WikipediaQueryRun , DuckDuckGoSearchResults
from tools import CurrentDateTimeTool, ShippingTimeEstimator, PromoCodeScraper , calculator , get_current_location , scrape_and_crawl
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from langgraph.config import get_store
from langmem import create_prompt_optimizer





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
tools=[wiki_tool,CurrentDateTimeTool,ShippingTimeEstimator,PromoCodeScraper,DuckDuckGo,Google_search,calculator,get_current_location,scrape_and_crawl]

store = InMemoryStore()

def prompt(state):
    item = store.get(("instructions",), key="agent_instructions")
    instructions = item.value["prompt"]
    sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
    return [sys_prompt] + state['messages']
    
def agent(prompt):
    
    store.put(("instructions",), key="agent_instructions", value={"prompt": "Help customer to find it's product and solve it's problem give the actual products"})

    agent = create_react_agent("gpt-4o", prompt=prompt, tools=tools, store=store)

    # prompt=input("Enter Query: ")

    result = agent.invoke(
        {"messages": [
            {"role": "user", "content" :prompt}]}
    )

    optimizer = create_prompt_optimizer("gpt-4o")

    current_prompt = store.get(("instructions",), key="agent_instructions").value["prompt"]
    feedback = {"request": "Always sign off from Shoppin Fashon AI; Enjoy Shopping see you soon!!"}

    optimizer_result = optimizer.invoke({"prompt": current_prompt, "trajectories": [(result["messages"], feedback)]})
    
    store.put(("instructions",), key="agent_instructions", value={"prompt": optimizer_result})

    result = agent.invoke(
        {"messages": [
            {"role": "user", "content" :prompt}]}
    )


    return result['messages'][-1].pretty_print()