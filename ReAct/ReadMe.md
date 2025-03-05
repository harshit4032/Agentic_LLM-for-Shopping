<div align="justify">
# Virtual Shopping Assistant using ReAct

## Overview
This virtual shopping assistant is designed for fashion e-commerce platforms, leveraging advanced LLMs, search tools, and decision-making techniques to enhance the shopping experience. The assistant can search for fashion products, compare prices, check for discounts, estimate shipping times, and verify return policies.

## Features
- **Product Search & Comparison**: Uses Google Search API, FireCrawl, and Tavily to find and compare fashion products.
- **Discount & Offer Checks**: Identifies applicable discounts and coupons.
- **Shipping & Return Policy Verification**: Estimates shipping time and ensures return policies align with user preferences.
- **Multi-Agent Decision Making**: Implements techniques like ReAct, ReST, Chain of Tools, and MultiAgent multitooling for enhanced decision-making.
- **Local & API-based LLM Integration**: Uses GPT-3.5-turbo, GPT-4o, LLaMA-3.2 (locally), and LLaMA-3-70B-8192 via APIs.

## Technology Stack
- **Programming Language**: Python
- **Frameworks & Libraries**: LangChain, Ollama, Gorq, Hugging Face, LangGraph, LangSmith, PhiData
- **LLM Integration**: OpenAI, Meta (LLaMA)
- **Search & Data Retrieval**: Google Search API, FireCrawl, WolframAlpha, Tavily
- **Decision Making**: ReAct, ReST, Chain of Tools, MultiAgent multitooling

## Files & Structure
- `agent.py`: Core logic for agent-based decision-making using LLMs.
- `tools.py`: Implements external tools like search APIs and discount finders.
- `results.py`: Processes and formats the outputs from various tools.
- `ReAct_process.txt`: Logs and step-by-step execution details of the ReAct methodology.

## Setup & Installation
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd virtual-shopping-assistant
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the assistant**:
   ```bash
   python agent.py
   ```

## Usage
- Provide the assistant with search queries (e.g., "Find a floral skirt under $40 in size S").
- The agent will fetch results, compare options, and check for discounts.
- Results are displayed in a structured format with direct purchase links.

## Future Enhancements
- Improved memory handling for past interactions.
- Expanding product categories and supported marketplaces.
- Enhancing response time and model accuracy.
  /div>



