import httpx
import json

async def handle_llm_and_push(prompt: str):
    try:
        # Call summary service
        res = await httpx.post("http://localhost/summary", json={"prompt": prompt}, timeout=10.0)
        summary = res.json().get("summary", "No summary available.")
    except Exception as e:
        summary = f"⚠️ Failed to retrieve data for: {prompt}"

    # Push via WebSocket to all clients
    await ws_manager.broadcast(json.dumps({
        "type": "llm_result",
        "prompt": prompt,
        "slm": f"Hi there 👋! Let me get that for you...\n\n{summary}",
        "layout": [],
        "next": []
    }))
