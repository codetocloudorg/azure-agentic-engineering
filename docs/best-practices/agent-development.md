# Agent Development Best Practices

This guide covers best practices for developing AI agents using Microsoft Agent Framework and Azure AI Foundry.

> **Maintained by [Code to Cloud](https://github.com/codetocloudorg)**

## 🎯 Core Principles

### 1. Design for Observability

Use the Agent 365 Observability SDK for comprehensive telemetry:

```bash
# Install observability packages
pip install microsoft-agents-a365-observability-core
pip install microsoft-agents-a365-observability-extensions-agent-framework
```

```python
from microsoft_agents_a365.observability.core.config import configure
from microsoft_agents_a365.observability.extensions.agentframework.trace_instrumentor import (
    AgentFrameworkInstrumentor,
)

# Configure observability
configure(
    service_name="my-production-agent",
    service_namespace="ai.agents"
)

# Enable auto-instrumentation (traces agent invocations, tool calls, inference)
AgentFrameworkInstrumentor().instrument()

# Your agent code is now automatically traced!
```

**Environment Variables:**
```bash
ENABLE_OBSERVABILITY=true
ENABLE_A365_OBSERVABILITY_EXPORTER=true  # Export to Agent 365 service (false = console)
```

> ⚠️ **Note:** Agent 365 Observability is part of the [Frontier preview program](https://adoption.microsoft.com/copilot/frontier-program/).

📖 [Agent 365 Observability Documentation](https://learn.microsoft.com/microsoft-agent-365/developer/observability)

#### Alternative: Manual OpenTelemetry

For more control, use OpenTelemetry directly:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set up tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Trace agent operations
with tracer.start_as_current_span("agent_execution") as span:
    span.set_attribute("agent.name", agent.name)
    span.set_attribute("agent.model", agent.model)
    response = await agent.run(query)
```

### 2. Implement Proper Error Handling

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def run_agent_with_retry(agent, query: str):
    try:
        return await agent.run(query)
    except RateLimitError:
        logger.warning("Rate limited, retrying...")
        raise
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise
```

### 3. Use Managed Identity

Never use API keys in production:

```python
from azure.identity import DefaultAzureCredential

# ✅ Good: Use managed identity
credential = DefaultAzureCredential()

agent = AzureOpenAIResponsesClient(
    credential=credential,
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
).as_agent(name="SecureAgent")

# ❌ Bad: Hardcoded API key
# client = AzureOpenAI(api_key="sk-...")
```

## 🏗️ Agent Architecture Patterns

### Pattern 1: Single Agent with Tools

Best for: Simple, focused tasks

```python
from agent_framework import Agent
from agent_framework.tools import function_tool

@function_tool
def search_documents(query: str) -> list[str]:
    """Search the document index."""
    # Implementation
    pass

@function_tool
def create_summary(text: str) -> str:
    """Summarize the provided text."""
    # Implementation
    pass

agent = Agent(
    name="DocumentAnalyzer",
    instructions="You analyze documents and provide summaries.",
    tools=[search_documents, create_summary]
)
```

### Pattern 2: Multi-Agent Workflow

Best for: Complex, multi-step processes

```python
from agent_framework.workflows import Workflow, Graph

# Define specialized agents
planner = Agent(name="Planner", instructions="Break down tasks...")
researcher = Agent(name="Researcher", instructions="Find information...")
writer = Agent(name="Writer", instructions="Create content...")

# Create workflow graph
workflow = Workflow.from_graph(
    Graph()
    .add_node("plan", planner)
    .add_node("research", researcher)
    .add_node("write", writer)
    .add_edge("plan", "research")
    .add_edge("research", "write")
)

# Execute workflow
result = await workflow.run("Create a report on Azure AI services")
```

### Pattern 3: Human-in-the-Loop

Best for: High-stakes decisions requiring approval

```python
from agent_framework import Agent, HumanApprovalRequired

async def process_with_approval(agent: Agent, query: str):
    response = await agent.run(query)
    
    if response.requires_approval:
        approval = await get_human_approval(response.proposed_action)
        if approval:
            return await agent.execute_approved_action(response)
        else:
            return await agent.run("The user rejected this action. Suggest alternatives.")
    
    return response
```

## 🔧 SDK Usage Guidelines

### Microsoft Agent Framework

```python
# Installation
# pip install agent-framework --pre

from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential
import os

# Initialize with environment variables
agent = AzureOpenAIResponsesClient(
    endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    credential=DefaultAzureCredential()
).as_agent(
    name="ProductionAgent",
    instructions="""You are a helpful assistant that:
    1. Provides accurate information
    2. Cites sources when available
    3. Admits uncertainty when unsure
    """
)
```

### Azure AI Foundry SDK

```python
# Installation
# pip install azure-ai-projects azure-identity openai

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Connect to project
project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_ENDPOINT"],
    credential=DefaultAzureCredential()
)

# Get OpenAI-compatible client
openai_client = project.inference.get_azure_openai_client(
    api_version="2024-10-21"
)

# Use the Responses API
response = openai_client.responses.create(
    model="gpt-4o",
    input="Explain Azure AI services"
)
```

## 📊 Monitoring & Logging

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

async def monitored_agent_call(agent, query: str):
    logger.info(
        "agent_call_started",
        agent_name=agent.name,
        query_length=len(query)
    )
    
    start_time = time.time()
    try:
        response = await agent.run(query)
        logger.info(
            "agent_call_completed",
            agent_name=agent.name,
            duration_ms=(time.time() - start_time) * 1000,
            token_usage=response.usage.total_tokens
        )
        return response
    except Exception as e:
        logger.error(
            "agent_call_failed",
            agent_name=agent.name,
            error=str(e)
        )
        raise
```

### Metrics Collection

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)

agent_calls = meter.create_counter(
    "agent.calls",
    description="Number of agent invocations"
)

agent_latency = meter.create_histogram(
    "agent.latency",
    description="Agent response time in ms"
)

token_usage = meter.create_counter(
    "agent.tokens",
    description="Token usage by agent"
)
```

## ✅ Testing Strategies

### Unit Testing Agents

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_agent_responds_to_greeting():
    agent = Agent(
        name="TestAgent",
        instructions="Respond politely to greetings"
    )
    
    # Mock the LLM call
    agent._client.run = AsyncMock(return_value="Hello! How can I help?")
    
    response = await agent.run("Hello")
    assert "Hello" in response or "Hi" in response
```

### Integration Testing

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_tool_execution():
    @function_tool
    def add_numbers(a: int, b: int) -> int:
        return a + b
    
    agent = Agent(
        name="MathAgent",
        tools=[add_numbers]
    )
    
    response = await agent.run("What is 5 + 3?")
    assert "8" in response
```

## 🚫 Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded prompts | Inflexible, hard to update | Use configuration files or environment variables |
| No rate limiting | Service abuse, cost overruns | Implement token-based rate limiting |
| Synchronous calls | Poor performance at scale | Use async/await patterns |
| No timeout handling | Hanging requests | Set explicit timeouts on all calls |
| Single point of failure | System unavailability | Implement fallback strategies |

## 📚 Additional Resources

- [Agent Framework Documentation](https://learn.microsoft.com/agent-framework/)
- [Azure AI Foundry SDK Overview](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
