"""
AI Agent framework implementation.

An agent that can reason, use tools, and execute tasks.
"""
import json
import time
import re
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Tool:
    """A tool that the agent can use."""
    name: str
    description: str
    func: Callable
    parameters: dict = field(default_factory=dict)


@dataclass
class Message:
    """A message in the conversation."""
    role: str  # system, user, assistant, tool
    content: str
    tool_calls: List[dict] = field(default_factory=list)
    tool_call_id: Optional[str] = None


class Agent:
    """AI Agent with tool-use capability."""

    def __init__(self, name: str = "Agent"):
        self.name = name
        self.tools: Dict[str, Tool] = {}
        self.messages: List[Message] = []
        self.memory: Dict[str, Any] = {}

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    def add_system_message(self, content: str):
        self.messages.append(Message(role="system", content=content))

    def think(self, user_input: str) -> str:
        """Process input and decide what to do."""
        self.messages.append(Message(role="user", content=user_input))

        # Simple reasoning: parse for tool calls
        response = self._reason(user_input)

        # Check if response contains tool calls
        tool_calls = self._parse_tool_calls(response)
        if tool_calls:
            for tc in tool_calls:
                tool_name = tc["name"]
                tool_args = tc["arguments"]

                if tool_name in self.tools:
                    tool = self.tools[tool_name]
                    try:
                        result = tool.func(**tool_args)
                        result_str = json.dumps(result) if not isinstance(result, str) else result
                    except Exception as e:
                        result_str = f"Error: {e}"

                    self.messages.append(Message(
                        role="tool", content=result_str,
                        tool_call_id=tc.get("id", tool_name)
                    ))
                else:
                    self.messages.append(Message(
                        role="tool", content=f"Tool '{tool_name}' not found",
                        tool_call_id=tc.get("id", tool_name)
                    ))

            # Generate final response after tool use
            final_response = self._generate_final()
            self.messages.append(Message(role="assistant", content=final_response))
            return final_response

        self.messages.append(Message(role="assistant", content=response))
        return response

    def _reason(self, user_input: str) -> str:
        """Simple reasoning - simulates thinking."""
        # Check direct answers
        user_input_lower = user_input.lower()

        if "hello" in user_input_lower or "hi" in user_input_lower:
            return f"Hello! I'm {self.name}. How can I help you today?"

        if "help" in user_input_lower:
            tools_desc = "\n".join(
                f"  - {t.name}: {t.description}"
                for t in self.tools.values()
            )
            return f"I have access to these tools:\n{tools_desc}"

        # Tool detection patterns
        for tool_name, tool in self.tools.items():
            if tool_name.lower() in user_input_lower:
                return f"I'll use the {tool_name} tool to help with that."

        # Check memory
        for key, value in self.memory.items():
            if key.lower() in user_input_lower:
                return f"From memory: {key} = {value}"

        return f"I understand you want to: {user_input}. Let me process that."

    def _parse_tool_calls(self, text: str) -> List[dict]:
        """Parse tool calls from text - simulates LLM function calling."""
        calls = []
        for tool_name in self.tools:
            if f"use the {tool_name} tool" in text.lower():
                calls.append({
                    "name": tool_name,
                    "arguments": {"query": text},
                    "id": tool_name,
                })
        return calls

    def _generate_final(self) -> str:
        """Generate final response after tool execution."""
        last_tool_msg = None
        for msg in reversed(self.messages):
            if msg.role == "tool":
                last_tool_msg = msg
                break

        if last_tool_msg:
            return f"Done! The result is: {last_tool_msg.content[:100]}"
        return "Task completed."

    def remember(self, key: str, value: Any):
        self.memory[key] = value

    def recall(self, key: str) -> Optional[Any]:
        return self.memory.get(key)


def main():
    print("=== AI Agent Framework ===\n")

    agent = Agent("Assistant")

    # Register tools
    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression."""
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters in expression"
        try:
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {e}"

    def get_time(query: str) -> str:
        """Get current time."""
        return f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    def search_knowledge(query: str) -> str:
        """Search my knowledge base."""
        knowledge = {
            "python": "Python is a high-level programming language created by Guido van Rossum.",
            "ai": "AI stands for Artificial Intelligence.",
            "weather": "I can't check weather without internet access.",
        }
        for key, value in knowledge.items():
            if key in query.lower():
                return value
        return f"I don't have information about '{query}' in my knowledge base."

    agent.register_tool(Tool("calculator", "Calculate mathematical expressions", calculator))
    agent.register_tool(Tool("get_time", "Get current date and time", get_time))
    agent.register_tool(Tool("search", "Search my knowledge base", search_knowledge))

    # System prompt
    agent.add_system_message(
        f"You are {agent.name}, an AI assistant with access to tools. "
        "Help users by using your tools and knowledge."
    )

    # Conversations
    conversations = [
        "Hello!",
        "What tools do you have?",
        "Calculate 15 * 3 + 8",
        "What is the current time?",
        "Tell me about Python",
        "What is AI?",
    ]

    print("Conversations:")
    for msg in conversations:
        print(f"\n  User: {msg}")
        response = agent.think(msg)
        print(f"  {agent.name}: {response}")

    # Memory
    print("\n=== Agent Memory ===")
    agent.remember("user_name", "Alice")
    agent.remember("last_topic", "Python")
    print(f"  Remembered: {agent.recall('user_name')}")
    print(f"  Remembered: {agent.recall('last_topic')}")

    print("\n=== Agent Framework Features ===")
    print("  1. Tool registration and execution")
    print("  2. Memory management")
    print("  3. Thought/reasoning process")
    print("  4. Multi-turn conversation")
    print("  5. Extensible tool system")
    print("  Production: LangChain, AutoGPT, CrewAI")


if __name__ == "__main__":
    main()
