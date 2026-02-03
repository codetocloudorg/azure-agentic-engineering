# Azure AI Architecture Best Practices

This directory contains architecture guides and reference patterns for building AI solutions on Azure.

> **Maintained by [Code to Cloud](https://github.com/codetocloudorg)**

---

## 🏗️ Deploy an AI Landing Zone

> **Ready to deploy?** Use these official Microsoft accelerators:

| Accelerator | Description | Deploy |
|-------------|-------------|--------|
| **Azure AI Landing Zones** | Enterprise-scale reference architecture with Bicep & Terraform | [➡️ GitHub](https://github.com/Azure/AI-Landing-Zones) |
| **Deploy AI in Production** | Full stack with AI Foundry, Fabric, Search, Purview (~45 min) | [➡️ GitHub](https://github.com/microsoft/Deploy-Your-AI-Application-In-Production) |

---

## 📚 Official Azure Architecture Resources

### AI/ML Reference Architectures

Browse the complete collection at [Azure Architecture Center - AI + Machine Learning](https://learn.microsoft.com/azure/architecture/browse/?azure_categories=ai-machine-learning).

#### Featured Architectures

| Architecture | Description |
|-------------|-------------|
| [Baseline Microsoft Foundry Chat](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat) | Network-secured, highly available chat applications |
| [Foundry Chat in Landing Zone](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone) | Enterprise deployment with Azure Landing Zones |
| [Multi-Agent Workflow Automation](https://learn.microsoft.com/azure/architecture/ai-ml/idea/multiple-agent-workflow-automation) | Scalable multi-agent systems with Agent Framework |
| [Conversation Knowledge Mining](https://learn.microsoft.com/azure/architecture/ai-ml/idea/unlock-insights-from-conversational-data) | Extract insights from conversational data |

## 🏗️ Architecture Patterns

### 1. AI Landing Zone Pattern

The AI Landing Zone is a secure, resilient foundation for AI workloads:

```
┌────────────────────────────────────────────────────────────────┐
│                    Management Subscription                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Azure       │  │  Log         │  │  Automation  │         │
│  │  Monitor     │  │  Analytics   │  │  Account     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│                    Connectivity Subscription                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Hub VNet    │  │  Azure       │  │  ExpressRoute│         │
│  │              │  │  Firewall    │  │  /VPN        │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│                    AI Landing Zone Subscription                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Spoke VNet                              │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐            │  │
│  │  │AI Foundry  │ │ AI Search  │ │  Storage   │            │  │
│  │  │ Project    │ │            │ │  Account   │            │  │
│  │  └────────────┘ └────────────┘ └────────────┘            │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐            │  │
│  │  │ Key Vault  │ │ Container  │ │ App Service│            │  │
│  │  │            │ │ Registry   │ │ / ACA      │            │  │
│  │  └────────────┘ └────────────┘ └────────────┘            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

**Key Components:**
- **Azure AI Foundry**: Unified AI development platform
- **Azure AI Search**: RAG and knowledge retrieval
- **Private Endpoints**: All services network-isolated
- **Managed Identity**: Credential-free authentication

📖 [AI Landing Zones Repository](https://github.com/Azure/AI-Landing-Zones)

### 2. RAG (Retrieval-Augmented Generation) Pattern

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   User Query    │────▶│   Embedding     │────▶│   Vector        │
│                 │     │   Model         │     │   Search        │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Response      │◀────│   LLM           │◀────│   Context       │
│                 │     │   (GPT-4o)      │     │   Augmentation  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Implementation Options:**
1. **Azure AI Search + OpenAI**: Best for enterprise document search
2. **Microsoft Fabric + OneLake**: Best for analytics-heavy workloads
3. **Cosmos DB + Vector Search**: Best for real-time applications

### 3. Multi-Agent Workflow Pattern

```
┌───────────────────────────────────────────────────────────────┐
│                     Agent Orchestrator                         │
│                   (Agent Framework)                            │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Planning   │  │  Execution  │  │  Validation │          │
│  │   Agent     │  │    Agent    │  │    Agent    │          │
│  │             │  │             │  │             │          │
│  │ - Analyze   │  │ - Code Gen  │  │ - Review    │          │
│  │ - Decompose │  │ - API Calls │  │ - Test      │          │
│  │ - Prioritize│  │ - File Ops  │  │ - Feedback  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                       Shared Context                          │
│              (State, Memory, Tool Registry)                   │
└───────────────────────────────────────────────────────────────┘
```

📖 [Agent Framework Documentation](https://learn.microsoft.com/agent-framework/)

## 🎯 Design Checklist

Use the [AI Landing Zones Design Checklist](https://github.com/Azure/AI-Landing-Zones/blob/main/docs/AI-Landing-Zones-Design-Checklist.md) to evaluate your architecture against:

### Cloud Adoption Framework Areas
- [ ] Strategy & Planning
- [ ] Ready (Landing Zone)
- [ ] Adopt (Migrate/Innovate)
- [ ] Govern
- [ ] Manage

### Well-Architected Framework Pillars
- [ ] Reliability
- [ ] Security
- [ ] Cost Optimization
- [ ] Operational Excellence
- [ ] Performance Efficiency

## 📖 Additional Resources

- [Cloud Adoption Framework - AI Scenario](https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/ai/)
- [Well-Architected Framework - AI Workloads](https://learn.microsoft.com/azure/well-architected/ai/)
- [Azure AI Services Documentation](https://learn.microsoft.com/azure/ai-services/)
