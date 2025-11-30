import asyncio
from google.genai import types

from google.adk.runners import Runner
from google.adk.plugins import LoggingPlugin
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

from config import APP_NAME, USER_ID
from agents import final_agent, test_load_memory_agent
from config.settings import SESSION_ID
from utils import handle_response_stream

# ==========================================
# Sessions (short-term memory)
# ==========================================
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

# ==========================================
# MAIN
# ==========================================
async def main1():
    # Create a session
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="session1"
    )
    await memory_service.add_session_to_memory(session)

    # Run the pipeline with session (short-term memory), memory (long-term) and Observability: Logging, Tracing, Metrics
    runner = Runner(agent=final_agent,
                    app_name=APP_NAME,
                    session_service=session_service,
                    memory_service=memory_service,
                    plugins=[LoggingPlugin()])

    response = await runner.run_debug(
        "Search today's maximum of ten news about Bitcoin and Ethereum."
    )
    print("\nFINAL SUMMARY WITH SESSION:\n", response)

    # Create a new runner with the updated cryptoApp
    test_load_memory_runner = Runner(
        agent=test_load_memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    test_load_memory_runner = await runner.run_debug(
        "What is today's Bitcoin_trend"
    )

async def main():
    # Create a session
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    await memory_service.add_session_to_memory(session)

    # Run the pipeline with session (memory)
    runner = Runner(agent=final_agent,
                    app_name=APP_NAME,
                    session_service=session_service,
                    memory_service=memory_service,
                    plugins=[LoggingPlugin()])

    message_content = types.Content(
        role="user",
        parts=[types.Part(text="Search today's maximum of ten news about Bitcoin and Ethereum")]
    )

    response_stream = runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message_content
    )

    await handle_response_stream(response_stream)

    # Test memory
    message_test_content = types.Content(
        role="user",
        parts=[types.Part(text="What is today's Bitcoin_trend")]
    )

    test_load_memory_runner = Runner(
        agent=test_load_memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    test_memory_runner = test_load_memory_runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message_test_content
    )

    await handle_response_stream(test_memory_runner)

# ==========================================
# EXECUTE
# ==========================================
if __name__ == "__main__":
    asyncio.run(main())