import asyncio
from backend.ws.websocket_server import emit_live_status, emit_metric_update

async def simulate():
    await emit_live_status()
    await emit_metric_update("CPU_Usage", 74.3)
    await emit_metric_update("Memory_MB", 10600.5)

if __name__ == "__main__":
    asyncio.run(simulate())
