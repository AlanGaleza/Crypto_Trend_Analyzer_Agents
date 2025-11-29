import asyncio
from google.adk.runners import Runner
from google.adk.plugins import LoggingPlugin
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

from config import APP_NAME, USER_ID
from agents import final_agent, test_load_memory_agent
# ==========================================
# Sessions (short-term memory)
# ==========================================
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

# ==========================================
# MAIN
# ==========================================
async def main():
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

# ==========================================
# EXECUTE
# ==========================================
if __name__ == "__main__":
    asyncio.run(main())