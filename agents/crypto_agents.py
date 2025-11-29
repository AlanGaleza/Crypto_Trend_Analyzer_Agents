from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

from config import retry_config
from tools import analyze

# ==========================================
# GOOGLE SEARCH - BTC
# ==========================================
bitcoin_search_agent = LlmAgent(
    name="bitcoin_search_agent",
    description="Agent searches for latest news/posts specifically about Bitcoin.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="Search for today's news about Bitcoin only. Use google_search.",
    tools=[google_search],
    output_key="bitcoin_search",
)

# ==========================================
# GOOGLE SEARCH - ETH
# ==========================================
ethereum_search_agent = LlmAgent(
    name="ethereum_search_agent",
    description="Agent searches for latest news/posts specifically about Ethereum.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="Search for today's news about Ethereum only. Use google_search.",
    tools=[google_search],
    output_key="ethereum_search",
)

# ==========================================
# SENTIMENT AGENTY — BTC
# ==========================================
bitcoin_sentiment_agent = LlmAgent(
    name="bitcoin_sentiment_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Analyzes sentiment of posts related to Bitcoin.",
    instruction="""
    Take the Bitcoin posts from bitcoin_search_agent.
    Pass posts to the analyze tool.
    Return ONLY sentiment results.
    """,
    tools=[AgentTool(agent=bitcoin_search_agent), analyze],
    output_key="bitcoin_sentiment",
)

# ==========================================
# SENTIMENT AGENTY — ETH
# ==========================================
ethereum_sentiment_agent = LlmAgent(
    name="ethereum_sentiment_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Agent searches for latest news/posts specifically about Ethereum.",
    instruction="""
    Take the Ethereum posts from ethereum_search_agent.
    Pass posts to the analyze tool.
    Return ONLY sentiment results.
    """,
    tools=[AgentTool(agent=ethereum_search_agent), analyze],
    output_key="ethereum_sentiment",
)

# ==========================================
# PARALLEL WORKFLOW
# ==========================================
crypto_parallel = ParallelAgent(
    name="crypto_parallel_workflow",
    description="Runs Bitcoin and Ethereum pipelines in parallel and returns both sentiment results.",
    sub_agents=[
        SequentialAgent(
            name="btc_pipeline",
            sub_agents=[bitcoin_search_agent, bitcoin_sentiment_agent]
        ),
        SequentialAgent(
            name="eth_pipeline",
            sub_agents=[ethereum_search_agent, ethereum_sentiment_agent]
        )
    ]
)

# ==========================================
# SUMMARY AGENT
# ==========================================
summary_agent = LlmAgent(
    name="summary_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Aggregates Bitcoin and Ethereum sentiment results and determines overall trend.",
    instruction="""
    You receive output from two pipelines:
    - bitcoin_sentiment
    - ethereum_sentiment

    Your tasks:

    1. Determine the trend for each cryptocurrency based on sentiment results:
       - More positive → bullish
       - More negative → bearish
       - Mixed → neutral

    2. Output JSON:
    {
      "Bitcoin_trend": "...",
      "Ethereum_trend": "...",
      "explanation": {
        "Bitcoin": "...",
        "Ethereum": "..."
      }
    }
    """,
    output_key="summary",
)

# ==========================================
# FINAL SEQUENTIAL PIPELINE
# ==========================================
final_agent = SequentialAgent(
    name="crypto_master_pipeline",
    sub_agents=[
        crypto_parallel,
        summary_agent
    ],
    description="Runs crypto_parallel workflow and then aggregates results using summary_agent."
)