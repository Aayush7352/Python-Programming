"""
WebSocket demonstration using asyncio and websockets.

Requires: pip install websockets
"""
import sys
import asyncio
import json
import time


def main():
    """WebSocket demo with echo server and client."""
    try:
        import websockets
        from websockets.server import serve
    except ImportError:
        print("websockets is not installed.")
        print("Install with: pip install websockets")
        print("\nThis file demonstrates WebSocket patterns.")
        sys.exit(1)

    print("=== WebSocket Demo ===")

    connected_clients = set()
    message_history = []

    async def chat_handler(websocket):
        """Handle a WebSocket connection."""
        connected_clients.add(websocket)
        client_id = id(websocket)
        print(f"\n  Client {client_id} connected")

        try:
            async for raw_message in websocket:
                try:
                    data = json.loads(raw_message)
                except json.JSONDecodeError:
                    data = {"type": "text", "content": raw_message}

                timestamp = time.time()

                # Create response
                response = {
                    "type": data.get("type", "text"),
                    "sender": client_id,
                    "content": data.get("content", raw_message),
                    "timestamp": timestamp,
                    "message_id": len(message_history),
                }

                message_history.append(response)

                # Echo back to sender
                await websocket.send(json.dumps({
                    **response,
                    "event": "echo",
                }))

                # Broadcast to all other clients
                if data.get("broadcast", False):
                    for client in connected_clients:
                        if client != websocket:
                            try:
                                await client.send(json.dumps({
                                    **response,
                                    "event": "broadcast",
                                }))
                            except websockets.exceptions.ConnectionClosed:
                                pass

                # Send count of connected clients
                await websocket.send(json.dumps({
                    "type": "system",
                    "event": "clients",
                    "count": len(connected_clients),
                }))

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            connected_clients.discard(websocket)
            print(f"  Client {client_id} disconnected")

    async def run_server():
        """Start the WebSocket server."""
        async with serve(chat_handler, "localhost", 8765):
            print("  WebSocket server started on ws://localhost:8765")
            print("  (Server will run for 5 seconds for demo)")
            await asyncio.sleep(5)

    async def run_client():
        """Connect a client and send messages."""
        await asyncio.sleep(0.5)
        try:
            async with websockets.connect("ws://localhost:8765") as websocket:
                print("\n  Client connected, sending messages...")

                messages = [
                    {"type": "text", "content": "Hello WebSocket!", "broadcast": False},
                    {"type": "text", "content": "Broadcast this!", "broadcast": True},
                    {"type": "command", "content": "/status"},
                ]

                for msg in messages:
                    await websocket.send(json.dumps(msg))
                    print(f"  Sent: {msg['content']}")
                    response = await websocket.recv()
                    parsed = json.loads(response)
                    print(f"  Received: {parsed.get('event')} - {parsed.get('content')}")
                    await asyncio.sleep(0.5)

        except (ConnectionRefusedError, OSError) as e:
            print(f"  Could not connect: {e}")

    async def demo():
        """Run server and client concurrently."""
        server_task = asyncio.create_task(run_server())
        client_task = asyncio.create_task(run_client())

        await asyncio.gather(client_task, server_task)

    # Run the demo
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        pass

    print("\n\n=== WebSocket Summary ===")
    print(f"  Total messages exchanged: {len(message_history)}")
    print("\n  WebSocket features:")
    print("  1. Full-duplex communication")
    print("  2. Low latency (no HTTP overhead)")
    print("  3. Persistent connection")
    print("  4. Supports binary and text frames")
    print("  5. Built-in ping/pong for keep-alive")


if __name__ == "__main__":
    main()
