# 4️⃣ Next Steps

Congratulations! 🎉 You've built and deployed your first AI agent on Azure.

---

## 🎯 What You've Accomplished

- ✅ Set up your development environment
- ✅ Built an AI agent with the Microsoft Agent Framework
- ✅ Deployed to Azure with proper security
- ✅ Learned the fundamentals of agentic AI on Azure

---

## 🗺️ Where to Go From Here

### 📚 Dive Deeper into This Repo

| Topic | Guide | Description |
|-------|-------|-------------|
| **Architecture** | [Architecture Best Practices](../architecture/) | Reference architectures, AI Landing Zones |
| **Agent Patterns** | [Agent Development](../best-practices/agent-development.md) | Multi-agent workflows, tools, error handling |
| **Security** | [Security Best Practices](../security/security-best-practices.md) | Private endpoints, RBAC, governance |
| **Deployment** | [Production Deployment](../deployment/production-deployment.md) | CI/CD, IaC, monitoring |
| **SDKs** | [SDK Reference](../sdks/) | Agent Framework, Foundry SDK, Copilot SDK |

---

### 🔧 Advanced Topics

#### Multi-Agent Workflows

Build systems where multiple agents collaborate:

```python
from agent_framework.workflows import Workflow, Graph

# Create specialized agents
planner = create_agent("Planner", "Break down complex tasks")
researcher = create_agent("Researcher", "Find information")
writer = create_agent("Writer", "Create content")

# Connect them in a workflow
workflow = Workflow.from_graph(
    Graph()
    .add_node("plan", planner)
    .add_node("research", researcher)
    .add_node("write", writer)
    .add_edge("plan", "research")
    .add_edge("research", "write")
)

result = await workflow.run("Create a report on Azure AI")
```

📖 [See full example](../../samples/workflows/multi_agent_workflow.py)

---

#### Add Observability

Monitor your agents in production:

```python
from microsoft_agents_a365.observability.core.config import configure
from microsoft_agents_a365.observability.extensions.agentframework.trace_instrumentor import (
    AgentFrameworkInstrumentor,
)

# Configure observability
configure(service_name="my-agent", service_namespace="production")

# Enable auto-instrumentation
AgentFrameworkInstrumentor().instrument()
```

📖 [Agent 365 Observability Docs](https://learn.microsoft.com/microsoft-agent-365/developer/observability)

---

#### Deploy an AI Landing Zone

For enterprise-scale deployments:

```bash
git clone https://github.com/Azure/AI-Landing-Zones.git
cd AI-Landing-Zones/bicep
azd up
```

📖 [AI Landing Zones Repository](https://github.com/Azure/AI-Landing-Zones)

---

#### Building Developer Tools? Try Copilot SDK

If you're building **developer-focused tools** (CLIs, IDE extensions, code review bots), the GitHub Copilot SDK might be a better fit:

```typescript
import { CopilotClient, defineTool } from "@github/copilot-sdk";

// Define a custom tool
const reviewCode = defineTool("review_code", {
    description: "Review code for issues",
    parameters: {
        type: "object",
        properties: {
            code: { type: "string", description: "The code to review" },
        },
        required: ["code"],
    },
    handler: async ({ code }) => {
        // Your review logic here
        return { issues: [], suggestions: ["Add type hints"] };
    },
});

const client = new CopilotClient();
const session = await client.createSession({
    model: "gpt-4.1",
    tools: [reviewCode],
});

const response = await session.sendAndWait({ 
    prompt: "Review this function for issues..." 
});
console.log(response?.data.content);

await client.stop();
```

📖 [Full Copilot SDK Tutorial](../sdks/copilot-sdk.md) | [When to Use What](../sdks/README.md#-which-sdk-should-i-use)

---

### 📖 Official Microsoft Resources

| Resource | Description |
|----------|-------------|
| [Agent Framework Docs](https://learn.microsoft.com/agent-framework/) | Official documentation |
| [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) | Platform documentation |
| [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/browse/?azure_categories=ai-machine-learning) | Reference architectures |
| [Cloud Adoption Framework](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/ai/) | Enterprise guidance |

---

## 💬 Join the Community

| Platform | Link |
|----------|------|
| 🎮 **Discord** | [Join Code to Cloud](https://discord.gg/codetocloud) |
| 🐙 **GitHub** | [Code to Cloud Org](https://github.com/codetocloudorg) |
| 💬 **Discussions** | [Ask Questions](https://github.com/codetocloudorg/azure-agentic-engineering/discussions) |

---

## 🤝 Contribute

Found something to improve? We'd love your help!

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

📖 [Contributing Guide](../../CONTRIBUTING.md)

---

<div align="center">

## 🚀 Happy Building!

**You're now ready to build amazing AI agents on Azure.**

[← Back to Main README](../../README.md)

</div>
