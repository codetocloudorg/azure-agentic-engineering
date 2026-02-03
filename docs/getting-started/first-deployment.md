# 3️⃣ Deploy to Azure

Now let's deploy your agent to Azure for production use.

---

## 🎯 What You'll Deploy

A production-ready setup with:
- Azure OpenAI for the LLM
- Azure Container Apps for hosting
- Managed Identity for secure auth
- Application Insights for monitoring

---

## 🚀 Option 1: Quick Deploy with azd (Recommended)

The fastest way to get to production:

```bash
# Clone the production accelerator
git clone --recurse-submodules \
  https://github.com/microsoft/Deploy-Your-AI-Application-In-Production.git

cd Deploy-Your-AI-Application-In-Production

# Login and deploy (~45 minutes)
azd auth login
azd up
```

This deploys:
- ✅ Azure AI Foundry
- ✅ Azure AI Search
- ✅ Microsoft Fabric (optional)
- ✅ Microsoft Purview (governance)
- ✅ Private networking
- ✅ Managed identities

📖 [Full Deployment Guide](https://github.com/microsoft/Deploy-Your-AI-Application-In-Production/blob/main/docs/DeploymentGuide.md)

---

## 🏗️ Option 2: Deploy Infrastructure Only

If you want just the core AI infrastructure from this repo:

```bash
cd azure-agentic-engineering/infra/bicep

# Get your principal ID
PRINCIPAL_ID=$(az ad signed-in-user show --query id -o tsv)

# Deploy
az deployment group create \
  --resource-group rg-my-agents \
  --template-file main.bicep \
  --parameters principalId=$PRINCIPAL_ID environmentName=dev
```

This creates:
- Azure OpenAI with GPT-4o
- Azure AI Search
- Key Vault
- Storage Account
- Log Analytics

---

## 🐳 Option 3: Containerize Your Agent

Package your agent as a container for Azure Container Apps:

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### requirements.txt

```
agent-framework>=1.0.0b1
azure-identity>=1.15.0
fastapi>=0.109.0
uvicorn>=0.27.0
```

### main.py (API wrapper)

```python
from fastapi import FastAPI
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential
import os

app = FastAPI()

credential = DefaultAzureCredential()
agent = AzureOpenAIResponsesClient(
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    credential=credential,
).as_agent(
    name="ProductionAgent",
    instructions="You are a helpful assistant."
)

@app.post("/chat")
async def chat(message: str):
    response = await agent.run(message)
    return {"response": response}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Deploy to Container Apps

```bash
# Build and push
az acr build --registry myregistry --image my-agent:v1 .

# Deploy
az containerapp create \
  --name my-agent \
  --resource-group rg-my-agents \
  --image myregistry.azurecr.io/my-agent:v1 \
  --target-port 8000 \
  --ingress external \
  --env-vars AZURE_OPENAI_ENDPOINT=https://... \
  --user-assigned /subscriptions/.../my-identity
```

---

## ✅ Post-Deployment Checklist

After deploying, verify everything works:

- [ ] **Health check**: `curl https://your-app.azurecontainerapps.io/health`
- [ ] **Test chat**: `curl -X POST https://your-app.../chat?message=Hello`
- [ ] **Check logs**: Azure Portal → Container Apps → Logs
- [ ] **Monitor**: Azure Portal → Application Insights

---

## 🔒 Security Checklist

Before going live:

- [ ] Using Managed Identity (no API keys)
- [ ] Private endpoints enabled (for production)
- [ ] HTTPS only
- [ ] RBAC configured with least privilege
- [ ] Diagnostic logging enabled
- [ ] Content Safety enabled (if user-facing)

---

## 💰 Cost Considerations

| Resource | Approximate Cost |
|----------|------------------|
| Azure OpenAI (GPT-4o) | ~$0.005/1K tokens |
| Container Apps | ~$0.000024/vCPU-second |
| AI Search (Basic) | ~$75/month |
| Key Vault | ~$0.03/10K operations |

> 💡 Use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) for estimates.

---

## ➡️ Next Step

Your agent is deployed! Let's explore what's next.

**[Continue to: Next Steps →](next-steps.md)**
