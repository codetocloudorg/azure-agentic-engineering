# GitHub Copilot Instructions for Azure Agentic Engineering Repository

## Overview

This repository contains best practices, architecture patterns, and implementation guides for Azure AI services with a GitHub-first DevOps approach.

## Repository Context

- **Organization**: [Code to Cloud](https://github.com/codetocloudorg)
- **Focus Areas**:
  - **Azure AI Platforms**: Azure AI Foundry, Azure OpenAI, AI Landing Zones
  - **Agentic AI**: Microsoft Agent Framework, multi-agent workflows
  - **GitHub-First DevOps**: GitHub Actions, GitHub Copilot SDK, not Azure DevOps
- **Primary SDKs**: Microsoft Agent Framework, Azure AI Foundry SDK, GitHub Copilot SDK

## Code Generation Guidelines

### General Principles

1. **Security First**: Never include secrets, API keys, or credentials in code. Always use:
   - Azure Managed Identity
   - Azure Key Vault
   - Environment variables with `.env.example` templates
   - `DefaultAzureCredential` for authentication

2. **Azure Best Practices**: Follow Azure Well-Architected Framework principles:
   - Reliability
   - Security
   - Cost Optimization
   - Operational Excellence
   - Performance Efficiency

### Python Development

```python
# Always use async patterns for AI operations
import asyncio
from azure.identity import DefaultAzureCredential

# Prefer structured logging
import logging
logging.basicConfig(level=logging.INFO)

# Use type hints
from typing import Optional, List, Dict, Any
```

### .NET Development

```csharp
// Use dependency injection
// Implement IAsyncDisposable for AI clients
// Use CancellationToken for all async operations
```

### Infrastructure as Code

- **Prefer Bicep** for Azure infrastructure
- Use Azure Verified Modules (AVM) when available
- Implement proper resource tagging
- Enable diagnostic settings for all resources

## SDK-Specific Guidelines

### Microsoft Agent Framework

```python
# pip install agent-framework --pre
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential

# Always use credential-based authentication
credential = DefaultAzureCredential()
```

### Azure AI Foundry SDK

```python
# pip install azure-ai-projects azure-identity openai
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential()
)
```

### GitHub Copilot SDK

```python
# pip install github-copilot-sdk
# Requires Copilot CLI installed
```

## Documentation Standards

- Use clear, concise language
- Include architecture diagrams where applicable
- Provide code examples in Python, .NET, or both
- Reference official Microsoft Learn documentation
- Include estimated costs and performance considerations

## Security Checklist

When generating code, always ensure:

- [ ] No hardcoded secrets or credentials
- [ ] Using Managed Identity where possible
- [ ] Private endpoints for production workloads
- [ ] RBAC with least privilege principle
- [ ] Network isolation considerations
- [ ] Data encryption at rest and in transit

## Architecture Patterns

Refer to these resources when designing solutions:

- [Azure AI Landing Zones](https://github.com/Azure/AI-Landing-Zones)
- [Deploy AI in Production](https://github.com/microsoft/Deploy-Your-AI-Application-In-Production)
- [Azure Architecture Center - AI/ML](https://learn.microsoft.com/azure/architecture/browse/?azure_categories=ai-machine-learning)

## Common Tasks

### Creating a New Agent

1. Choose the appropriate SDK (Agent Framework or Foundry)
2. Implement proper error handling and retry logic
3. Add observability (OpenTelemetry integration)
4. Include unit and integration tests

### Deploying to Production

1. Use Azure Developer CLI (`azd`) for deployment
2. Implement proper CI/CD with GitHub Actions
3. Enable monitoring and alerting
4. Configure auto-scaling where appropriate

## File Naming Conventions

- Python: `snake_case.py`
- .NET: `PascalCase.cs`
- Bicep/Terraform: `kebab-case.bicep`
- Documentation: `UPPER-CASE.md` for root docs, `kebab-case.md` for guides
