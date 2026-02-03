# 2️⃣ Your First Agent

Let's build a simple AI agent using the Microsoft Agent Framework.

---

## 🎯 What You'll Build

A conversational agent that:
- Connects to Azure OpenAI
- Uses secure authentication (no API keys!)
- Responds to user queries

---

## 📝 Create the Agent

Create a new file called `my_agent.py`:

```python
"""
My First Azure AI Agent
"""
import asyncio
import os
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential

async def main():
    # Use managed identity / Azure CLI credentials (no API keys!)
    credential = DefaultAzureCredential()
    
    # Create the agent
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        credential=credential,
    ).as_agent(
        name="MyFirstAgent",
        instructions="""You are a helpful AI assistant. 
        You provide clear, concise answers.
        You're friendly and professional."""
    )
    
    # Run the agent
    print("🤖 Agent is ready! Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break
        
        if not user_input:
            continue
        
        response = await agent.run(user_input)
        print(f"\n🤖 Agent: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔧 Configure Environment

Set your Azure OpenAI endpoint:

```bash
# Set environment variable
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"

# Login to Azure (for DefaultAzureCredential)
az login
```

---

## ▶️ Run the Agent

```bash
python my_agent.py
```

Expected output:
```
🤖 Agent is ready! Type 'quit' to exit.

You: Hello! What can you do?

🤖 Agent: Hello! I'm an AI assistant that can help you with a variety of tasks...

You: quit
Goodbye! 👋
```

---

## 🎉 Congratulations!

You just built your first AI agent! Let's understand what happened:

| Component | What It Does |
|-----------|--------------|
| `DefaultAzureCredential` | Authenticates without API keys (uses Azure CLI, managed identity, etc.) |
| `AzureOpenAIResponsesClient` | Connects to Azure OpenAI service |
| `.as_agent()` | Creates an agent with name and instructions |
| `agent.run()` | Sends a message and gets a response |

---

## 🔧 Add Tools (Optional)

Agents become powerful when they can use tools. Here's a quick example:

```python
from agent_framework.tools import function_tool

@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        # Safe evaluation of math expressions
        allowed = set("0123456789+-*/.() ")
        if all(c in allowed for c in expression):
            return str(eval(expression))
        return "Invalid expression"
    except:
        return "Error calculating"

# Add tools to your agent
agent = AzureOpenAIResponsesClient(
    endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    credential=credential,
).as_agent(
    name="ToolAgent",
    instructions="You are a helpful assistant with access to tools.",
    tools=[get_current_time, calculate]  # 👈 Add tools here
)
```

Now your agent can:
- Tell the time: *"What time is it?"*
- Do math: *"What's 15% of 250?"*

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `AZURE_OPENAI_ENDPOINT not set` | Run `export AZURE_OPENAI_ENDPOINT="https://..."` |
| `AuthenticationError` | Run `az login` to refresh credentials |
| `ResourceNotFound` | Check your endpoint URL is correct |
| `RateLimitError` | Wait a moment and try again |

---

## ➡️ Next Step

Your agent works locally! Let's deploy it to Azure for production use.

**[Continue to: Deploy to Azure →](first-deployment.md)**
