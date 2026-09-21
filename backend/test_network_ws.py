import asyncio
import websockets

from app.core.jwt import create_access_token

async def test():
    token = create_access_token({
        "sub": "1",
        "email": "mastertest@example.com",
        "role": "user",
    })

    uri = f"ws://127.0.0.1:8000/ws/network?token={token}"

    print("Connecting to ws://127.0.0.1:8000/ws/network...")

    async with websockets.connect(uri) as websocket:
        print("WEBSOCKET CONNECTED")

        for i in range(3):
            message = await websocket.recv()
            print(f"\nMESSAGE {i + 1}:")
            print(message)

asyncio.run(test())
