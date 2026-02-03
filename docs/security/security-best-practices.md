# Security Best Practices for Azure AI Applications

This guide covers security best practices for building and deploying AI applications on Azure.

## 🔐 Authentication & Authorization

### Use Managed Identity Everywhere

```python
from azure.identity import DefaultAzureCredential

# DefaultAzureCredential supports:
# - Environment variables
# - Workload Identity (AKS)
# - Managed Identity (Azure services)
# - Azure CLI (local development)
# - Visual Studio Code

credential = DefaultAzureCredential()
```

### RBAC Best Practices

| Role | Use Case | Scope |
|------|----------|-------|
| Azure AI User | Agent development | Project |
| Azure AI Project Manager | Project management | Project |
| Cognitive Services User | Consume AI services | Resource |
| Key Vault Secrets User | Read secrets | Key Vault |

```bash
# Assign role using Azure CLI
az role assignment create \
  --assignee <principal-id> \
  --role "Cognitive Services User" \
  --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>
```

### Never Use API Keys in Production

```python
# ❌ NEVER DO THIS
client = AzureOpenAI(api_key="sk-abc123...")

# ✅ ALWAYS DO THIS
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
client = AzureOpenAI(
    azure_ad_token_provider=lambda: credential.get_token(
        "https://cognitiveservices.azure.com/.default"
    ).token
)
```

## 🌐 Network Security

### Private Endpoints Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Internet                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Azure Front Door                          │
│                    (WAF Enabled)                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Virtual Network                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │               Application Subnet                         ││
│  │  ┌───────────────┐  ┌───────────────┐                  ││
│  │  │ Container App │  │ App Service   │                  ││
│  │  └───────────────┘  └───────────────┘                  ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │            Private Endpoint Subnet                       ││
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐            ││
│  │  │PE: OpenAI │ │PE: Search │ │PE: Storage│            ││
│  │  └───────────┘ └───────────┘ └───────────┘            ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Disable Public Access

```bicep
resource openAI 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: openAIName
  location: location
  properties: {
    publicNetworkAccess: 'Disabled'
    networkAcls: {
      defaultAction: 'Deny'
    }
  }
}
```

## 🔑 Secrets Management

### Azure Key Vault Integration

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://your-keyvault.vault.azure.net",
    credential=credential
)

# Retrieve secret
api_key = client.get_secret("openai-api-key").value
```

### Environment Variable Pattern

```python
# .env.example (commit this)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_KEY_VAULT_URL=https://your-keyvault.vault.azure.net

# .env (DO NOT commit - in .gitignore)
AZURE_OPENAI_ENDPOINT=https://actual-resource.openai.azure.com
# Note: No API keys needed with managed identity!
```

## 🛡️ Data Protection

### Encryption at Rest

All Azure AI services encrypt data at rest by default. For additional control:

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  properties: {
    encryption: {
      keySource: 'Microsoft.Keyvault'
      keyvaultproperties: {
        keyvaulturi: keyVault.properties.vaultUri
        keyname: encryptionKey.name
      }
    }
  }
}
```

### Encryption in Transit

Always use HTTPS/TLS 1.2+:

```python
import httpx

async with httpx.AsyncClient(
    http2=True,
    verify=True  # Always verify SSL certificates
) as client:
    response = await client.post(endpoint, json=data)
```

## 🔍 Content Safety

### Azure AI Content Safety Integration

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.identity import DefaultAzureCredential

content_safety_client = ContentSafetyClient(
    endpoint="https://your-content-safety.cognitiveservices.azure.com",
    credential=DefaultAzureCredential()
)

async def check_content_safety(text: str) -> bool:
    """Check if content is safe before processing."""
    result = content_safety_client.analyze_text(
        text=text,
        categories=["Hate", "Violence", "SelfHarm", "Sexual"]
    )
    
    # Block if any category exceeds threshold
    for category in result.categories_analysis:
        if category.severity >= 4:  # Threshold: 0-6 scale
            return False
    return True
```

### Input Validation

```python
from pydantic import BaseModel, validator

class UserQuery(BaseModel):
    message: str
    
    @validator('message')
    def validate_message(cls, v):
        if len(v) > 10000:
            raise ValueError('Message too long')
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
```

## 📝 Audit & Compliance

### Enable Diagnostic Logging

```bicep
resource diagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'audit-logs'
  scope: openAI
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        categoryGroup: 'allLogs'
        enabled: true
        retentionPolicy: {
          enabled: true
          days: 90
        }
      }
    ]
  }
}
```

### Audit Query Examples

```kusto
// All API calls to OpenAI
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.COGNITIVESERVICES"
| where Category == "RequestResponse"
| project TimeGenerated, CallerIpAddress, OperationName, ResultType
| order by TimeGenerated desc

// Failed authentication attempts
AzureDiagnostics
| where ResultType == "Failed"
| summarize count() by CallerIpAddress, bin(TimeGenerated, 1h)
| order by count_ desc
```

## ✅ Security Checklist

### Pre-Deployment

- [ ] Managed Identity configured
- [ ] Key Vault provisioned for any secrets
- [ ] Private endpoints enabled
- [ ] Public access disabled
- [ ] RBAC roles assigned (least privilege)
- [ ] Network Security Groups configured
- [ ] Content Safety enabled

### Post-Deployment

- [ ] Diagnostic logging enabled
- [ ] Azure Defender for Cloud enabled
- [ ] Vulnerability scanning configured
- [ ] Penetration testing scheduled
- [ ] Incident response plan documented
- [ ] Regular access reviews scheduled

## 🚨 Incident Response

### Security Alert Handling

```python
import logging
from azure.monitor.query import LogsQueryClient

async def check_security_alerts():
    client = LogsQueryClient(DefaultAzureCredential())
    
    query = """
    SecurityAlert
    | where TimeGenerated > ago(1h)
    | where Severity in ("High", "Critical")
    | project AlertName, Description, RemediationSteps
    """
    
    result = await client.query_workspace(
        workspace_id=WORKSPACE_ID,
        query=query,
        timespan="PT1H"
    )
    
    for row in result.tables[0].rows:
        logging.critical(f"Security Alert: {row[0]} - {row[1]}")
```

## 📚 Additional Resources

- [Azure Security Baseline for AI Services](https://learn.microsoft.com/security/benchmark/azure/baselines/cognitive-services-security-baseline)
- [Azure AI Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Microsoft Cloud Security Benchmark](https://learn.microsoft.com/security/benchmark/azure/)
- [Azure Policy for AI Services](https://learn.microsoft.com/azure/ai-services/cognitive-services-policy)
