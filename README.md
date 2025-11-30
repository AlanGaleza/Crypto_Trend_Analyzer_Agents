# Crypto Trend Analyzer using Multi-Agent Pipelines
<img src="resources/images/AIImageCrypto_Trend_Analyzer.png" width="200">

## Subtitle
Predicting Bitcoin and Ethereum trends using AI agents with session-based memory.

---

## Problem
Cryptocurrency markets move rapidly and are influenced by a massive amount of online news and social media posts.  
Manual tracking of trends is time-consuming, error-prone, and requires expertise. Investors and analysts need an automated tool to analyze sentiment trends in real-time to make better decisions.

---

## Solution
We designed a multi-agent AI system that:  
1. Searches for the latest news and posts about Bitcoin and Ethereum.  
2. Performs sentiment analysis on each post using a custom sentiment analyzer tool.  
3. Aggregates results to determine whether the overall trend is bullish, bearish, or neutral.  
4. Uses **short-term session memory** to maintain context during a user's session.  

---

## Value
- Provides near real-time sentiment trends for cryptocurrencies.  
- Leverages **multi-agent architecture** to parallelize pipelines (Bitcoin vs. Ethereum).  
- Integrates session-based memory to recall previous searches or analyses.  
- Offers a foundation for extending to additional cryptocurrencies or financial assets.  

---

## Architecture

### Overview
The system consists of:

1. **Parallel Agent Workflow:** Two pipelines running in parallel:  
   - **Sequential Agent Workflow: Bitcoin pipeline:** `bitcoin_search_agent` → `bitcoin_sentiment_agent`  
   - **Sequential Agent Workflow: Ethereum pipeline:** `ethereum_search_agent` → `ethereum_sentiment_agent`  

2. **Summary Agent:** Aggregates sentiment results and outputs a JSON trend report.

3. **Session Management:** `InMemorySessionService` maintains short-term memory across agent executions.

4. **User Agent:** Can query session memory to recall past trends or analytics using `load_memory`.

### ASCII Diagram
               +--------------------------+
               |   User Query / Runner    |
               +-----------+--------------+
                           |
                           v
                   +----------------+
                   | crypto_parallel|
                   +-------+--------+
                           |
              +------------+---------------+
              |                            | 
    +--------------------+      +----------------------+
    | Bitcoin Pipeline   |      | Ethereum Pipeline    |
    | search -> sentiment|      | search -> sentiment  |
    +--------------------+      +----------------------+
              |                            |
              +-------------+--------------+
                            |
                            v
                    +---------------+
                    | summary_agent |
                    +---------------+
                            |
                            v
                Trend Analysis JSON Output

---

## Features
- **Agent Tools:** `analyze_tool` for sentiment analysis, `load_memory` for recalling past sessions.  
- **Parallel Agents:** Bitcoin and Ethereum pipelines run concurrently.  
- **Sequential Agents:** Ensures stepwise execution of search → sentiment → summary aggregation.  
- **Session & Memory Integration:** Maintains short-term context for agent execution.  
- **Logging & Observability:** `LoggingPlugin` provides tracking of agent execution.  

---

## Installation & Setup

1. Clone this repository or download it:

```bash
git clone https://github.com/AlanGaleza/Crypto_Trend_Analyzer_Agents.git
cd CryptoApp
(Optional) Create and activate virtual environment
bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

Install dependencies:
bash
pip install -r requirements.txt
Set your Google API Key in environment variables (if not already set):

bash
# Windows (PowerShell)
setx GOOGLE_API_KEY "YOUR_API_KEY"
# macOS / Linux
export GOOGLE_API_KEY="YOUR_API_KEY"

Run the main script:
bash
python main.py
````
License
MIT License

---