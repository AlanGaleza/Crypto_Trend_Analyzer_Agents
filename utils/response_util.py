async def handle_response_stream(response_stream):
    async for event in response_stream:
        try:
            if hasattr(event, 'text') and event.text:
                print(event.text, end="", flush=True)

            elif hasattr(event, 'part') and hasattr(event.part, 'text'):
                print(event.part.text, end="", flush=True)

            elif hasattr(event, 'content') and event.content.parts:
                print(event.content.parts[0].text, end="", flush=True)

        except Exception as e:
            print(f"\n[Stream Error] {e}")