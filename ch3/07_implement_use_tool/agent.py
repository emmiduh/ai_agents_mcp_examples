import asyncio
import os
from pathlib import Path

import google.generativeai as genai
from client import MCPClient
from dotenv import load_dotenv

load_dotenv()

# Load Gemini API key
LLM_API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=LLM_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

mcp_client = MCPClient(
    name="calculator_server_connection",
    command="uv",
    server_args=[
        "--directory",
        str(Path(__file__).parent.parent.resolve()),
        "run",
        "calculator_server.py",
    ],
)

print("Welcome to your AI Assistant. Type 'goodbye' to quit.")


async def main():
    """Main async function to run the assistant."""
    await mcp_client.connect()
    available_tools = await mcp_client.get_available_tools()
    print(
        f"Available tools: {', '.join([tool['name'] for tool in available_tools])}"
    )

    while True:
        prompt = input("You: ")
        if prompt.lower() == "goodbye":
            print("AI Assistant: Goodbye!")
            break

        response = model.generate_content(prompt)
        print(f"Assistant: {response.text}")

    await mcp_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
