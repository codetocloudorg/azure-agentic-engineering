# 1️⃣ Prerequisites

Before you start building AI agents, you'll need to set up your development environment.

---

## 🔧 Required Tools

### Azure Account

You need an Azure subscription with access to Azure OpenAI Service.

```bash
# Login to Azure
az login

# Verify your subscription
az account show
```

> 💡 **No Azure account?** [Create a free account](https://azure.microsoft.com/free/) with $200 credit.

---

### Azure CLI

Install the Azure CLI for managing Azure resources.

| Platform | Command |
|----------|---------|
| macOS | `brew install azure-cli` |
| Windows | `winget install Microsoft.AzureCLI` |
| Linux | `curl -sL https://aka.ms/InstallAzureCLIDeb \| sudo bash` |

Verify installation:
```bash
az --version  # Should be 2.61.0 or later
```

---

### Azure Developer CLI (azd)

Install `azd` for streamlined deployments.

| Platform | Command |
|----------|---------|
| macOS | `brew install azd` |
| Windows | `winget install Microsoft.Azd` |
| Linux | `curl -fsSL https://aka.ms/install-azd.sh \| bash` |

Verify installation:
```bash
azd version  # Should be 1.15.0 or later
```

---

### Python 3.10+

Install Python for running agent code.

| Platform | Command |
|----------|---------|
| macOS | `brew install python@3.12` |
| Windows | `winget install Python.Python.3.12` |
| Linux | `sudo apt install python3.12` |

Verify installation:
```bash
python3 --version  # Should be 3.10 or later
```

---

### .NET 8+ (Optional)

Install .NET if you prefer C# development.

| Platform | Command |
|----------|---------|
| macOS | `brew install dotnet` |
| Windows | `winget install Microsoft.DotNet.SDK.8` |
| Linux | [See .NET docs](https://learn.microsoft.com/dotnet/core/install/linux) |

Verify installation:
```bash
dotnet --version  # Should be 8.0 or later
```

---

## 📦 Install SDKs

Create a virtual environment and install the core SDKs:

```bash
# Create project directory
mkdir my-agent-project && cd my-agent-project

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install SDKs
pip install agent-framework --pre
pip install azure-ai-projects azure-identity openai
```

For .NET:
```bash
dotnet new console -n MyAgentProject
cd MyAgentProject
dotnet add package Microsoft.Agents.AI --prerelease
```

---

## ✅ Verify Your Setup

Run this quick check to make sure everything is ready:

```bash
# Check all tools
echo "=== Environment Check ==="
az --version | head -1
azd version
python3 --version
echo "=== All Good! ==="
```

Expected output:
```
=== Environment Check ===
azure-cli                         2.67.0
azd version 1.15.0
Python 3.12.x
=== All Good! ===
```

---

## 🔑 Azure OpenAI Access

You'll need an Azure OpenAI resource. If you don't have one:

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new **Azure OpenAI** resource
3. Deploy a model (e.g., `gpt-4o`)
4. Note your endpoint URL

Or use the CLI:
```bash
# Create resource group
az group create --name rg-my-agents --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name my-openai-resource \
  --resource-group rg-my-agents \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

---

## ➡️ Next Step

Your environment is ready! Let's build your first agent.

**[Continue to: Your First Agent →](first-agent.md)**
