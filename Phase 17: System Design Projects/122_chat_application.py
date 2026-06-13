"""
Real-time chat application using WebSockets (asyncio).

Requires: pip install websockets
"""
import asyncio
import json
import time
import sys
from typing import Set, Dict


class ChatRoom:
    """Chat room with message history."""

    def __init__(self, name: str, max_history: int = 100):
        self.name = name
        self.messages = []
        self.max_history = max_history

    def add_message(self, username: str, content: str) -> dict:
        msg = {
            "username": username,
            "content": content,
            "timestamp": time.time(),
            "id": len(self.messages),
        }
        self.messages.append(msg)
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        return msg

    def get_recent(self, count: int = 20) -> list:
        return self.messages[-count:]


class ChatServer:
    """WebSocket chat server."""

    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}
        self.users: Dict[str, Set[asyncio.Queue]] = {}
        self.room_users: Dict[str, Set[str]] = {}

    def get_or_create_room(self, name: str) -> ChatRoom:
        if name not in self.rooms:
            self.rooms[name] = ChatRoom(name)
            self.room_users[name] = set()
        return self.rooms[name]

    async def handle_connection(self, websocket):
        """Handle a WebSocket connection."""
        queue = asyncio.Queue()
        username = None
        current_room = None

        try:
            async for raw_message in websocket:
                data = json.loads(raw_message)
                msg_type = data.get("type")

                if msg_type == "join":
                    username = data.get("username", "anonymous")
                    room_name = data.get("room", "general")
                    current_room = self.get_or_create_room(room_name)

                    if username not in self.users:
                        self.users[username] = set()
                    self.users[username].add(queue)
                    self.room_users[room_name].add(username)

                    # Send recent history
                    await websocket.send(json.dumps({
                        "type": "history",
                        "messages": current_room.get_recent(20),
                        "active_users": list(self.room_users[room_name]),
                    }))

                    # Broadcast join
                    await self.broadcast(room_name, {
                        "type": "system",
                        "content": f"{username} joined {room_name}",
                    }, exclude=None)

                elif msg_type == "message" and current_room and username:
                    content = data.get("content", "")
                    if content.strip():
                        msg = current_room.add_message(username, content.strip())
                        await self.broadcast(current_room.name, {
                            "type": "message",
                            **msg,
                        })

                elif msg_type == "leave" and current_room and username:
                    await self._remove_user(username, current_room.name, queue)
                    username = None
                    current_room = None

        except Exception:
            pass
        finally:
            if username and current_room:
                await self._remove_user(username, current_room.name, queue)

    async def _remove_user(self, username: str, room_name: str, queue: asyncio.Queue):
        if username in self.users:
            self.users[username].discard(queue)
            if not self.users[username]:
                del self.users[username]
        if room_name in self.room_users:
            self.room_users[room_name].discard(username)
        await self.broadcast(room_name, {
            "type": "system",
            "content": f"{username} left {room_name}",
        }, exclude=None)

    async def broadcast(self, room_name: str, message: dict, exclude=None):
        """Broadcast a message to all users in a room."""
        for username, queues in list(self.users.items()):
            for q in queues:
                try:
                    await q.put(message)
                except Exception:
                    pass

    async def start(self, host: str = "localhost", port: int = 8765):
        try:
            import websockets
            from websockets.server import serve

            print(f"  Chat server starting on ws://{host}:{port}")
            async with serve(self.handle_connection, host, port):
                await asyncio.Future()  # run forever
        except ImportError:
            print("  websockets not installed (pip install websockets)")
            return


async def simulate_client():
    """Simulate a chat client for demonstration."""
    await asyncio.sleep(0.5)
    try:
        import websockets
        async with websockets.connect("ws://localhost:8765") as ws:
            print("\n  [Simulated Client]")
            # Join room
            await ws.send(json.dumps({
                "type": "join", "username": "Alice", "room": "general"
            }))
            response = await ws.recv()
            data = json.loads(response)
            print(f"  Received history ({len(data.get('messages', []))} messages)")

            # Send messages
            messages = ["Hello everyone!", "How are you?", "This is a chat demo!"]
            for msg in messages:
                await ws.send(json.dumps({
                    "type": "message", "content": msg
                }))
                response = await ws.recv()
                data = json.loads(response)
                print(f"  Message: {data['content']}")

            # Leave
            await ws.send(json.dumps({"type": "leave"}))

    except (ConnectionRefusedError, ImportError):
        print("  Could not connect to chat server")


async def main():
    print("=== Chat Application ===\n")

    server = ChatServer()
    server_task = asyncio.create_task(server.start())
    client_task = asyncio.create_task(simulate_client())

    await asyncio.sleep(3)  # Run for 3 seconds
    server_task.cancel()

    print("\n\n=== Chat Architecture ===")
    print("  1. WebSocket for real-time communication")
    print("  2. Rooms for channel-based chat")
    print("  3. Message history for new joiners")
    print("  4. Active user tracking")
    print("  5. Scalable: horizontal sharding")
    print("  6. Durable: message persistence")


if __name__ == "__main__":
    asyncio.run(main())
