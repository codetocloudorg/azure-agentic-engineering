# Azure AI SDKs Reference Guide

This guide provides an overview of the key SDKs for building AI applications on Azure.

> **Maintained by [Code to Cloud](https://github.com/codetocloudorg)**

---

## 🎯 Which SDK Should I Use?

This is the question developers ask most. Here's the honest answer:

### Decision Flowchart

```
What are you building?
│
├── 🛠️ DEVELOPER TOOLS (CLI, IDE extensions, code assistants)
│   └── GitHub Copilot SDK
│       • Pre-built coding agent with file/git/terminal tools
│       • Requires Copilot subscription (or BYOK)
│
├── 🤖 CUSTOM AI AGENTS (any domain)
│   └── Microsoft Agent Framework
│       └── Need Azure models? → ALSO add Foundry SDK
│       • Multi-agent orchestration, workflows, graphs
│       • Full control over agent logic
│
├── ☁️ AZURE AI PLATFORM FEATURES (hosted agents, evaluations, tracing)
│   └── Azure AI Foundry SDK
│       • Managed agent runtime
│       • Cloud evaluations
│       • Built-in tracing
│
└── 📡 SIMPLE MODEL CALLS (just chat completions)
    └── OpenAI SDK or Foundry SDK
        • Direct inference, minimal setup
```

### The Key Insight

**These SDKs are complementary, not competing:**

| SDK | What It Does | ✅ Use When | ❌ Don't Use When |
|-----|--------------|-------------|-------------------|
| **[Agent Framework](https://github.com/microsoft/agent-framework)** | Build & orchestrate agents **in your code** | Multi-agent workflows, custom logic, graph-based orchestration | You just need simple chat completions |
| **[Foundry SDK](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview)** | Access Azure AI **platform services** | Hosted agents, cloud evaluations, tracing, Foundry direct models | You need cloud-agnostic code |
| **[Copilot SDK](copilot-sdk.md)** | Embed **Copilot's coding agent** | Developer tools, CLI assistants, code review bots | Non-developer domains (customer service, data, etc.) |
| **[OpenAI SDK](https://learn.microsoft.com/azure/ai-services/openai/)** | Direct **model inference** | Simple chat completions, max API compatibility | You need agent orchestration or Foundry features |

### Common Patterns

| I'm Building... | SDKs to Use | Why |
|-----------------|-------------|-----|
| Multi-agent system on Azure | Agent Framework + Foundry SDK | AF for orchestration, Foundry for model access |
| Simple chatbot | Foundry SDK or OpenAI SDK | No orchestration needed |
| Code review CLI tool | **Copilot SDK** | Built-in file/git tools, coding-focused |
| VS Code extension with AI | **Copilot SDK** | Developer context, tool calling included |
| Customer service agent | Agent Framework + Foundry SDK | Custom domain, needs your own logic |
| RAG application | Agent Framework + Foundry SDK | Need custom retrieval + generation flow |
| Data pipeline with AI | Agent Framework | Workflows, checkpointing, custom tools |

### ⚠️ Important Distinctions

| Feature | Agent Framework | Foundry SDK | Copilot SDK | OpenAI SDK |
|---------|----------------|-------------|-------------|------------|
| **Primary Use** | Build custom agents | Azure platform access | Developer tools | Model inference |
| **Where agents run** | Your code | Foundry cloud | Copilot CLI | N/A |
| **Multi-agent** | ✅ Native | ❌ Manual | ❌ | ❌ |
| **Cloud-agnostic** | ✅ | ❌ Azure only | ❌ GitHub | ⚠️ Azure/OpenAI |
| **Built-in tools** | ❌ Bring your own | ❌ | ✅ File, Git, Terminal | ❌ |
| **Custom tools** | ✅ | ✅ | ✅ | ✅ |
| **Workflows/Graphs** | ✅ | ❌ | ❌ | ❌ |
| **Production ready** | ✅ (Preview) | ✅ | ⚠️ Technical Preview | ✅ |

> **Source:** [Microsoft Foundry SDK Overview](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview)

---

## 📦 SDK Quick Reference

| SDK | Purpose | Languages | Install |
|-----|---------|-----------|---------|
| Agent Framework | Multi-agent orchestration | Python, .NET | `pip install agent-framework --pre` |
| Foundry SDK | Azure AI platform access | Python, .NET, JS | `pip install azure-ai-projects` |
| Copilot SDK | Embed Copilot in apps | Python, Node, .NET, Go | `pip install github-copilot-sdk` |
| OpenAI SDK | Direct model inference | Python, .NET, JS, Java | `pip install openai` |

---

## 🤖 Microsoft Agent Framework

A comprehensive framework for building, orchestrating, and deploying AI agents.

### ✅ Use When
- Building multi-agent systems with complex orchestration
- You need graph-based workflows with checkpointing
- You want cloud-agnostic code that works with any provider
- You need human-in-the-loop approval flows
- You want full control over agent logic

### ❌ Don't Use When
- You just need simple chat completions (use OpenAI SDK)
- You only need Azure-hosted agents without custom logic (use Foundry SDK)
- You're building developer tools (consider Copilot SDK)

### Installation

```bash
# Python
pip install agent-framework --pre

# .NET
dotnet add package Microsoft.Agents.AI --prerelease
```

### Quick Start (Python)

```python
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential

async def main():
    agent = AzureOpenAIResponsesClient(
        credential=DefaultAzureCredential()
    ).as_agent(
        name="AssistantBot",
        instructions="You are a helpful assistant."
    )
    
    response = await agent.run("What are the benefits of Azure AI?")
    print(response)

asyncio.run(main())
```

### Quick Start (.NET)

```csharp
using Microsoft.Agents.AI.OpenAI;
using Azure.Identity;

var agent = new OpenAIClient(
    new BearerTokenPolicy(new AzureCliCredential(), "https://ai.azure.com/.default"),
    new OpenAIClientOptions { Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1") })
    .GetOpenAIResponseClient("gpt-4o-mini")
    .AsAIAgent(name: "AssistantBot", instructions: "You are a helpful assistant.");

Console.WriteLine(await agent.RunAsync("What are the benefits of Azure AI?"));
```

### Key Features

- **Graph-based Workflows**: Connect agents with data flows
- **Streaming**: Real-time response streaming
- **Checkpointing**: Save and resume workflow state
- **Human-in-the-Loop**: Approval workflows
- **OpenTelemetry**: Built-in observability

📖 [Documentation](https://learn.microsoft.com/agent-framework/) | [GitHub](https://github.com/microsoft/agent-framework)

---

## 🏭 Azure AI Foundry SDK

Unified SDK for accessing Azure AI Foundry capabilities.

### ✅ Use When
- You need Azure-hosted agent runtime (Foundry Agent Service)
- You want cloud evaluations for your AI app
- You need built-in tracing and observability
- You want access to Foundry Direct models (non-Azure-OpenAI models)
- You're fine with Azure-only deployment

### ❌ Don't Use When
- You need cloud-agnostic code (use Agent Framework)
- You need multi-agent orchestration (use Agent Framework)
- You just need simple chat completions with max compatibility (use OpenAI SDK)
- You're building developer tools (consider Copilot SDK)

### Installation

```bash
pip install azure-ai-projects azure-identity openai
```

### Project Client

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Connect to your Foundry project
project = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential()
)
```

### OpenAI-Compatible Client

```python
# Get an OpenAI-compatible client from your project
openai_client = project.inference.get_azure_openai_client(api_version="2024-10-21")

# Use the Responses API
response = openai_client.responses.create(
    model="gpt-4o",
    input="Explain quantum computing in simple terms."
)
print(response.output_text)
```

### Capabilities

| Feature | Description |
|---------|-------------|
| Model Access | Azure OpenAI and Foundry Direct models |
| Agent Service | Hosted agent runtime |
| Cloud Evaluations | Run evaluations in the cloud |
| Tracing | Built-in application tracing |
| Fine-tuning | Custom model training |

📖 [Documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview)

---

## 🚀 GitHub Copilot SDK

> ⚠️ **Different use case!** Copilot SDK is for **developer tools**, not general AI agents. See [full guide](copilot-sdk.md).

Embed Copilot's coding-focused agent into your applications.

### When to Use Copilot SDK

| ✅ Use Copilot SDK For | ❌ Don't Use For |
|------------------------|------------------|
| CLI tools for developers | Customer service agents |
| VS Code extensions | Data processing pipelines |
| Code review bots | Enterprise RAG apps |
| Developer productivity tools | Any non-developer domain |

### Installation

```bash
# Python
pip install github-copilot-sdk

# Node.js
npm install @github/copilot-sdk

# .NET
dotnet add package GitHub.Copilot.SDK

# Go
go get github.com/github/copilot-sdk/go
```

### Quick Start (TypeScript)

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({ model: "gpt-4.1" });

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await client.stop();
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Built-in Tools** | File ops, Git, web requests, terminal |
| **Custom Tools** | Define your own tools Copilot can call |
| **BYOK** | Bring your own API keys (Azure, OpenAI, Anthropic) |
| **MCP Support** | Connect to Model Context Protocol servers |
| **Multi-language** | Python, TypeScript, Go, .NET |

📖 **[Full Copilot SDK Tutorial →](copilot-sdk.md)** | [GitHub](https://github.com/github/copilot-sdk)

---

## 🔧 Azure OpenAI SDK

Direct access to Azure OpenAI Service.

### ✅ Use When
- You just need simple chat completions
- You want maximum API compatibility with OpenAI
- You're migrating from OpenAI to Azure OpenAI
- You don't need Foundry-specific features (agents, evaluations)
- You want the most mature, stable SDK

### ❌ Don't Use When
- You need multi-agent orchestration (use Agent Framework)
- You want hosted agents or cloud evaluations (use Foundry SDK)
- You need Foundry Direct models via Responses API (use Foundry SDK)
- You're building developer tools (consider Copilot SDK)

### Installation

```bash
pip install openai
```

### With Azure Identity

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint="https://<resource>.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

📖 [Documentation](https://learn.microsoft.com/azure/ai-services/openai/)

---

## 🛠️ Azure Developer CLI (azd)

Streamline Azure development and deployment.

### Installation

```bash
# macOS
brew install azure/azd/azd

# Windows
winget install microsoft.azd

# Linux
curl -fsSL https://aka.ms/install-azd.sh | bash
```

### Key Commands

```bash
# Initialize a new project
azd init

# Provision and deploy
azd up

# Just provision infrastructure
azd provision

# Just deploy application
azd deploy

# Monitor your application
azd monitor

# Clean up resources
azd down
```

📖 [Documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)

---

## 📊 SDK Comparison Matrix

| Feature | Agent Framework | Foundry SDK | OpenAI SDK | Copilot SDK |
|---------|----------------|-------------|------------|-------------|
| **Primary Purpose** | Build & orchestrate agents | Access Foundry platform | Model inference | Embed Copilot |
| **Multi-Agent Orchestration** | ✅ Native (graphs) | ❌ | ❌ | ❌ |
| **Workflows** | ✅ Graph-based | ❌ | ❌ | ❌ |
| **Human-in-the-Loop** | ✅ | ❌ | ❌ | ❌ |
| **Checkpointing** | ✅ | ❌ | ❌ | ❌ |
| **Cloud-Agnostic** | ✅ | ❌ Azure only | ⚠️ Azure/OpenAI | ❌ GitHub |
| **Hosted Agent Service** | Via Foundry SDK | ✅ | ❌ | ❌ |
| **Cloud Evaluations** | Via Foundry SDK | ✅ | ❌ | ❌ |
| **Tracing/Observability** | ✅ OpenTelemetry | ✅ Built-in | ❌ | ✅ |
| **Foundry Direct Models** | Via Foundry SDK | ✅ | ✅ (Chat only) | ❌ |
| **Languages** | Python, .NET | Python, .NET, JS | All | Python, TS, Go, .NET |

### When They Work Together

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Application                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Microsoft Agent Framework                      │   │
│  │  • Define agents in code                                 │   │
│  │  • Multi-agent workflows (graphs)                        │   │
│  │  • Local orchestration                                   │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Azure AI Foundry SDK                        │   │
│  │  • Model access (Azure OpenAI, Foundry Direct)          │   │
│  │  • Cloud evaluations                                     │   │
│  │  • Tracing                                               │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Azure AI Foundry                       │   │
│  │  • GPT-4o, GPT-5.2, Foundry Direct Models               │   │
│  │  • Agent Service (hosted runtime)                        │   │
│  │  • Evaluations, Tracing, Fine-tuning                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Quick Links

- [Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Foundry SDK Docs](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview)
- [Copilot SDK GitHub](https://github.com/github/copilot-sdk)
- [Azure OpenAI Docs](https://learn.microsoft.com/azure/ai-services/openai/)
