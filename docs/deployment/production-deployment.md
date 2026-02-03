# Production Deployment Guide

This guide covers deploying AI applications to production using Azure Developer CLI (azd) and infrastructure as code.

## 🚀 Deployment Options

### Option 1: Azure Developer CLI (Recommended)

The fastest path to production using `azd`:

```bash
# Initialize project
azd init

# Deploy everything
azd up

# Deploy only infrastructure
azd provision

# Deploy only application
azd deploy
```

### Option 2: AI Landing Zone Accelerator

For enterprise deployments with full governance:

```bash
# Clone with submodules
git clone --recurse-submodules \
  https://github.com/microsoft/Deploy-Your-AI-Application-In-Production.git

cd Deploy-Your-AI-Application-In-Production

# Deploy (~45 minutes)
azd up
```

**What you get:**
- Azure AI Foundry with OpenAI models
- Microsoft Fabric with lakehouses
- Azure AI Search with vector search
- Microsoft Purview governance
- Private networking throughout

📖 [Deployment Guide](https://github.com/microsoft/Deploy-Your-AI-Application-In-Production/blob/main/docs/DeploymentGuide.md)

### Option 3: AI Landing Zone (IaC)

Deploy the foundation separately:

```bash
# Bicep
cd AI-Landing-Zones/bicep
az deployment sub create -l eastus -f main.bicep

# Terraform
cd AI-Landing-Zones/terraform
terraform init
terraform apply
```

📖 [AI Landing Zones Repository](https://github.com/Azure/AI-Landing-Zones)

## 📋 Pre-Deployment Checklist

### Azure Prerequisites

| Requirement | How to Check |
|-------------|--------------|
| Azure Subscription | `az account show` |
| Sufficient quota | Check Azure Portal → Quotas |
| Required permissions | Owner or Contributor + UAA |
| Azure CLI installed | `az --version` (≥2.61.0) |
| Azure Developer CLI | `azd version` (≥1.15.0) |

### Check Azure OpenAI Quota

```bash
# List current quota
az cognitiveservices account list-skus \
  --location eastus \
  --query "[?contains(name, 'OpenAI')]"
```

### Required RBAC Roles

| Role | Scope | Purpose |
|------|-------|---------|
| Contributor | Subscription | Create resources |
| User Access Administrator | Subscription | Assign roles |
| Azure AI User | Resource Group | Use AI services |

## 🏗️ Infrastructure as Code

### Bicep Template Structure

```
infra/
├── main.bicep              # Entry point
├── main.bicepparam         # Parameters
├── modules/
│   ├── ai-foundry.bicep   # AI Foundry resources
│   ├── networking.bicep   # VNets, private endpoints
│   ├── security.bicep     # Key Vault, RBAC
│   └── monitoring.bicep   # Log Analytics, App Insights
└── scripts/
    └── post-deploy.ps1    # Post-deployment configuration
```

### Example: AI Foundry Deployment

```bicep
// main.bicep
targetScope = 'resourceGroup'

param location string = resourceGroup().location
param environmentName string
param principalId string

module aiFoundry 'modules/ai-foundry.bicep' = {
  name: 'ai-foundry'
  params: {
    location: location
    name: 'aif-${environmentName}'
    principalId: principalId
  }
}

module privateEndpoints 'modules/networking.bicep' = {
  name: 'private-endpoints'
  params: {
    aiFoundryId: aiFoundry.outputs.id
    vnetId: networking.outputs.vnetId
  }
}
```

### Azure Developer CLI Configuration

```yaml
# azure.yaml
name: my-ai-app
metadata:
  template: azd-ai-starter

services:
  api:
    project: ./src/api
    language: python
    host: containerapp
    
  web:
    project: ./src/web
    language: typescript
    host: staticwebapp

infra:
  provider: bicep
  path: ./infra
```

## 🔒 Security Configuration

### Private Endpoints

All production deployments should use private endpoints:

```bicep
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-${serviceName}'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'plsc-${serviceName}'
        properties: {
          privateLinkServiceId: serviceId
          groupIds: [groupId]
        }
      }
    ]
  }
}
```

### Managed Identity Configuration

```bicep
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-${environmentName}'
  location: location
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, managedIdentity.id, 'Cognitive Services User')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'a97b65f3-24c7-4388-baec-2e87135dc908' // Cognitive Services User
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
```

## 📊 Monitoring Setup

### Application Insights Integration

```python
# Python application
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

configure_azure_monitor(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

tracer = trace.get_tracer(__name__)
```

### Log Analytics Queries

```kusto
// Agent performance metrics
customMetrics
| where name startswith "agent."
| summarize 
    avg_latency = avg(value),
    p95_latency = percentile(value, 95),
    call_count = count()
  by name, bin(timestamp, 1h)
| order by timestamp desc
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install azd
        uses: Azure/setup-azd@v1
        
      - name: Log in with Azure (Federated Credentials)
        run: |
          azd auth login \
            --client-id "${{ secrets.AZURE_CLIENT_ID }}" \
            --federated-credential-provider github \
            --tenant-id "${{ secrets.AZURE_TENANT_ID }}"
            
      - name: Provision Infrastructure
        run: azd provision --no-prompt
        env:
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          AZURE_ENV_NAME: ${{ github.ref == 'refs/heads/main' && 'prod' || 'staging' }}
          
      - name: Deploy Application
        run: azd deploy --no-prompt
```

## 🧪 Post-Deployment Validation

### Health Checks

```bash
# Check service health
curl https://your-app.azurewebsites.net/health

# Verify AI endpoint
curl -X POST https://your-ai-foundry.openai.azure.com/openai/deployments/gpt-4o/chat/completions \
  -H "Authorization: Bearer $(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### Smoke Tests

```python
import pytest
import httpx

@pytest.mark.smoke
async def test_agent_endpoint_responds():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/agent/chat",
            json={"message": "Hello"},
            timeout=30.0
        )
        assert response.status_code == 200
        assert "response" in response.json()
```

## 📚 Additional Resources

- [Azure Developer CLI Documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Deploy AI in Production Repository](https://github.com/microsoft/Deploy-Your-AI-Application-In-Production)
- [AI Landing Zones Repository](https://github.com/Azure/AI-Landing-Zones)
- [Azure Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
