# GitHub Copilot SDK Guide

> **Maintained by [Code to Cloud](https://github.com/codetocloudorg)**

## 🤔 Should I Use This SDK?

**First, be honest about your use case:**

| I Want To... | Use This? | Instead Use |
|--------------|-----------|-------------|
| **Embed Copilot's coding AI into my app** | ✅ Yes | - |
| **Build developer tools with AI assistance** | ✅ Yes | - |
| **Build custom AI agents for any domain** | ❌ No | [Agent Framework](https://github.com/microsoft/agent-framework) |
| **Call Azure AI models from my app** | ❌ No | [Foundry SDK](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) |
| **Build RAG or enterprise AI apps** | ❌ No | Agent Framework + Foundry SDK |

### The Key Difference

```
┌─────────────────────────────────────────────────────────────────┐
│  Copilot SDK                                                    │
│  • Pre-built coding-focused agent                               │
│  • File operations, Git, web requests built-in                  │
│  • Designed for developer tools                                 │
│  • Requires Copilot CLI + subscription (or BYOK)                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Agent Framework + Foundry SDK                                  │
│  • Build YOUR OWN custom agents                                 │
│  • Any domain (customer service, data analysis, etc.)           │
│  • Full control over agent logic                                │
│  • Uses Azure AI infrastructure                                 │
└─────────────────────────────────────────────────────────────────┘
```

**TL;DR:** Copilot SDK = embed Copilot in your app. Agent Framework = build your own agents.

---

## 📋 Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Copilot CLI** | [Installation guide](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli) |
| **Copilot Subscription** | Or use BYOK (Bring Your Own Key) |
| **Runtime** | Python 3.8+, Node.js 18+, Go 1.21+, or .NET 8.0+ |

```bash
# Verify CLI is installed
copilot --version
```

---

## 📦 Installation

```bash
# Python
pip install github-copilot-sdk

# Node.js / TypeScript
npm install @github/copilot-sdk

# Go
go get github.com/github/copilot-sdk/go

# .NET
dotnet add package GitHub.Copilot.SDK
```

---

## 🏗️ Architecture

The SDK communicates with Copilot CLI via JSON-RPC:

```
Your Application
       ↓
  SDK Client (manages lifecycle)
       ↓ JSON-RPC
  Copilot CLI (server mode)
       ↓
  GitHub Copilot Service
```

The SDK handles the CLI process automatically—you just write code.

---

## 🚀 Tutorial: Build Your First Copilot App

> ⚠️ **Note:** Examples below are from the official [getting-started guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md). Always refer to the latest SDK docs for API changes.

### Step 1: Hello Copilot (5 lines)

The simplest possible example:

**TypeScript:**
```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({ model: "gpt-4.1" });

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await client.stop();
process.exit(0);
```

**Python:** *(similar pattern)*
```python
from github_copilot_sdk import CopilotClient
import asyncio

async def main():
    client = CopilotClient()
    session = await client.create_session(model="gpt-4.1")
    
    response = await session.send_and_wait(prompt="What is 2 + 2?")
    print(response.data.content)
    
    await client.stop()

asyncio.run(main())
```

Run it:
```bash
# TypeScript
npx tsx hello_copilot.ts

# Python
python hello_copilot.py
```

Output:
```
4
```

---

### Step 2: Add Streaming

Make responses appear in real-time:

**TypeScript:**
```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    model: "gpt-4.1",
    streaming: true,
});

// Listen for response chunks
session.on("assistant.message_delta", (event) => {
    process.stdout.write(event.data.deltaContent);
});

session.on("session.idle", () => {
    console.log(); // New line when done
});

await session.sendAndWait({ prompt: "Tell me a short joke" });

await client.stop();
process.exit(0);
```

📖 See [Python SDK README](https://github.com/github/copilot-sdk/tree/main/python) for Python-specific syntax.

---

### Step 3: Add Custom Tools

**This is the powerful part.** Give Copilot the ability to call YOUR code:

**TypeScript:**
```typescript
import { CopilotClient, defineTool } from "@github/copilot-sdk";

// Define a tool that Copilot can call
const getWeather = defineTool("get_weather", {
    description: "Get the current weather for a city",
    parameters: {
        type: "object",
        properties: {
            city: { type: "string", description: "The city name" },
        },
        required: ["city"],
    },
    handler: async (args: { city: string }) => {
        const { city } = args;
        // In a real app, you'd call a weather API here
        const conditions = ["sunny", "cloudy", "rainy", "partly cloudy"];
        const temp = Math.floor(Math.random() * 30) + 50;
        const condition = conditions[Math.floor(Math.random() * conditions.length)];
        return { city, temperature: `${temp}°F`, condition };
    },
});

const client = new CopilotClient();
const session = await client.createSession({
    model: "gpt-4.1",
    streaming: true,
    tools: [getWeather],
});

session.on("assistant.message_delta", (event) => {
    process.stdout.write(event.data.deltaContent);
});

session.on("session.idle", () => {
    console.log();
});

// Copilot will call your tool to answer this!
await session.sendAndWait({
    prompt: "What's the weather like in Seattle and Tokyo?",
});

await client.stop();
process.exit(0);
```

📖 See [Python SDK README](https://github.com/github/copilot-sdk/tree/main/python) for Python-specific tool definition syntax.

**How it works:**
1. You define a tool with a name, description, and parameters
2. Copilot decides when to call your tool based on the user's question
3. SDK runs your handler function
4. Result is sent back to Copilot
5. Copilot incorporates the result into its response

---

## 🛠️ Built-in Tools

By default, the SDK enables all first-party Copilot tools (equivalent to `--allow-all` in CLI):

| Tool Category | Examples |
|---------------|----------|
| **File System** | Read, write, search files |
| **Git** | Commit, branch, diff |
| **Web** | HTTP requests |
| **Terminal** | Run commands |

You can customize which tools are enabled via SDK client options. Refer to the [SDK documentation](https://github.com/github/copilot-sdk) for details on tool configuration.

---

## 🔌 Connect to MCP Servers

[Model Context Protocol](https://modelcontextprotocol.io/) servers provide pre-built tools:

```typescript
const session = await client.createSession({
    mcpServers: {
        github: {
            type: "http",
            url: "https://api.githubcopilot.com/mcp/",
        },
    },
});
```

This gives Copilot access to GitHub repos, issues, and PRs!

---

## 👤 Create Custom Agents

Define specialized AI personas:

```typescript
const session = await client.createSession({
    customAgents: [{
        name: "pr-reviewer",
        displayName: "PR Reviewer",
        description: "Reviews pull requests for best practices",
        prompt: "You are an expert code reviewer. Focus on security, performance, and maintainability.",
    }],
});
```

---

## 🔑 BYOK (Bring Your Own Key)

Use your own API keys instead of a Copilot subscription. Supported providers include OpenAI, Azure, and Anthropic.

> 📖 Refer to the individual [SDK documentation](https://github.com/github/copilot-sdk) for BYOK configuration syntax, as it varies by language.

**With BYOK, you can use the SDK without GitHub authentication** by configuring your own API keys from supported LLM providers.

---

## ⚠️ Current Status

| Aspect | Status |
|--------|--------|
| **Maturity** | Technical Preview |
| **Production Ready** | Not yet recommended |
| **Billing** | Based on Copilot premium request quota |

---

## 🔗 Resources

| Resource | Link |
|----------|------|
| **GitHub Repo** | [github/copilot-sdk](https://github.com/github/copilot-sdk) |
| **Getting Started** | [Full Tutorial](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md) |
| **Cookbook** | [Recipes](https://github.com/github/awesome-copilot/blob/main/cookbook/copilot-sdk) |
| **Custom Instructions** | [awesome-copilot](https://github.com/github/awesome-copilot/blob/main/collections/copilot-sdk.md) |
| **MCP Documentation** | [MCP Guide](https://github.com/github/copilot-sdk/blob/main/docs/mcp.md) |

---

## ❓ FAQ

### Do I need a Copilot subscription?
Yes, unless using BYOK. There's a free tier with limited usage.

### How does billing work?
Each prompt counts toward your premium request quota.

### Can I use it in production?
It's in Technical Preview—not yet recommended for production.

### What models are supported?
All models available via Copilot CLI. Use `session.list_models()` to see available options.

---

## 🆚 Comparison: When to Use What

| Scenario | SDK |
|----------|-----|
| Build a CLI tool that helps devs write code | **Copilot SDK** |
| Build a VS Code extension with AI | **Copilot SDK** |
| Build a code review bot | **Copilot SDK** |
| Build a customer service agent | **Agent Framework** |
| Build a multi-agent data pipeline | **Agent Framework** |
| Call Azure OpenAI for RAG | **Foundry SDK** |
| Build any custom domain agent | **Agent Framework + Foundry SDK** |

**The bottom line:** Use Copilot SDK for **developer tools**, use Agent Framework for **everything else**.

---

<div align="center">

**[← Back to SDK Overview](README.md)**

</div>
