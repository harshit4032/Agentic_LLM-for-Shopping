

## **Features of the Multi-Agent, Multi-Tool, Self-Improvement Shopping Assistant using PhiData Agent**

This project showcases an advanced **Agentic LLM-based Shopping Assistant** built with **multi-agent**, **multi-tool**, and **self-improvement** capabilities to solve complex fashion e-commerce queries. Below are the key features highlighted from the system:

---

### **1. Dual Agent Integration:**
- **Gorq Agent (using LLaMA 3-70B)** [`gorq_agent.py`]:
  - Provides **structured outputs** for shopping recommendations.
  - Utilizes **Firecrawl**, **Google Search**, **DuckDuckGo**, and **WebsiteTools** for web crawling and product retrieval.
  - Handles **task-based trajectories** and saves them as JSON logs for replay and fine-tuning.

- **OpenAI Agent (using GPT-4o)** [`openai_agent.py`]:
  - Equipped with **reasoning** and **structured output** capabilities.
  - Integrates tools such as **Promo Code Scraper**, **Shipping Estimator**, **User Location Tool**, and more.
  - Handles complex reasoning and tool chaining for accurate and multi-step product searches.

---

### **2. Multi-Tool Capabilities:**
The agents can dynamically access and utilize multiple tools based on user queries:
- **Web Scraping** via **Firecrawl** and **WebsiteTools**.
- **Promo Code Extraction** from major coupon sites using the custom-built **PromoCodeScraper** [`tools.py`].
- **Shipping Estimation** with custom logic for delivery feasibility and timing.
- **Date & Time Retrieval**, **Calculator**, and **Location-based tools** to enrich contextual search.
- **Search Aggregation** using **Google**, **DuckDuckGo**, and other engines.

---

### **3. Task-Oriented Sample Trajectories:**
Implemented automated trajectory building covering real-world e-commerce use cases, such as:
- Finding products under budget with size constraints.
- Checking discount availability and promo code application.
- Comparing deals across platforms.
- Evaluating shipping timelines and return policies.
- These are saved in structured JSON format for downstream **fine-tuning** and **evaluation**.

---

### **4. Self-Improvement with Logging:**
- **Trajectory saving** and **result tracking** are integrated into every agent run, storing the query, reasoning, and final answer.
- Designed for iterative **agent refinement** through replaying trajectories and identifying failure points for improvement.

---

### **5. Real-Time Web Integration:**
Agents continuously retrieve **live product information**, **active discounts**, and **functional purchase links** via **API-driven** and **scraped** data sources, ensuring outputs are current and actionable.

---

### **6. Fault Handling and Error Awareness:**
- Implements **error logging** and detection of invalid schema responses (e.g., OpenAI API errors with function definitions).
- Displays user-friendly fallback outputs even when encountering tool or model failures.

---

### **7. Frontend Deployment:**
A **Streamlit** application [`app.py`] is included to provide an **interactive web interface** for real-time agent querying using the **OpenAI agent**.

---

### **8. Future-Ready Design:**
- Modular **tool architecture** for easy extension.
- Supports future scaling to additional agents, tools, and models.
- Lays groundwork for **RL-based optimizations** and **knowledge distillation**.

---

This system reflects a **robust, modular, and scalable architecture** aimed at delivering **intelligent shopping assistance** through **multi-step reasoning**, **external knowledge integration**, and **continuous self-improvement** using the latest **LLM-driven agent frameworks**.

