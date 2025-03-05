from typing import Annotated
from typing_extensions import TypedDict
import os
## Working With Tools
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import WikipediaAPIWrapper , DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper
from langchain_community.tools import WikipediaQueryRun , DuckDuckGoSearchResults
from tools import CurrentDateTimeTool, ShippingTimeEstimator, PromoCodeScraper , calculator , get_current_location , scrape_and_crawl
from langchain_core.tools import Tool
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode,tools_condition


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
def agent(user_input):
  ## Langgraph Application
  class State(TypedDict):
    messages:Annotated[list,add_messages]

  graph_builder= StateGraph(State)
  OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
  llm= ChatOpenAI(model_name="gpt-3.5-turbo")
  llm_with_tools=llm.bind_tools(tools=tools)
  def chatbot(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

  graph_builder.add_node("chatbot",chatbot)
  tool_node = ToolNode(tools=tools)
  graph_builder.add_node("tools", tool_node)

  graph_builder.add_conditional_edges(
      "chatbot",
      tools_condition,
  )
  graph_builder.add_edge("tools", "chatbot")
  graph_builder.add_edge(START,"chatbot")
  graph_builder.add_edge("chatbot",END)
  graph=graph_builder.compile()


  # user_input= input("Enter Query: ")

  events=graph.stream(
      {"messages": [("user", user_input)]},stream_mode="values"
  )

  res=[]
  for event in events:
    res.append(event["messages"][-1].pretty_print())
  
  return res
  