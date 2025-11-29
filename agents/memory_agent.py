from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.load_memory_tool import load_memory

from config import retry_config

# ==========================================
# USER AGENT (Access to load_memory tool)
# ==========================================
test_load_memory_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words. Use load_memory tool if you need to recall past conversations.",
    tools=[load_memory]
)