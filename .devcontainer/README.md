# GitHub Codespaces Container

This repository includes a fully configured development container for GitHub Codespaces.

## 🚀 Quick Start

1. Click the green **Code** button on GitHub
2. Select **Codespaces** tab
3. Click **Create codespace on main**

Your environment will be ready in ~2 minutes with the **Code to Cloud** banner!

## 📦 What's Included

### Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | AI/ML development, Azure SDKs |
| Azure CLI | Latest | Azure resource management |
| Azure Developer CLI (azd) | Latest | Infrastructure deployment |
| GitHub CLI | Latest | PR/issue management |

### Pre-installed Python Packages

```
azure-identity        # DefaultAzureCredential
azure-ai-projects     # Azure AI Foundry SDK
azure-ai-inference    # Model inference
agent-framework       # Microsoft Agent Framework (preview)
openai                # OpenAI SDK
python-dotenv         # Environment variables
```

### VS Code Extensions

| Category | Extensions |
|----------|------------|
| 🎨 Theme | GitHub Dark Default, Material Icons |
| 🤖 AI | GitHub Copilot, Copilot Chat |
| ☁️ Azure | Bicep, azd, Azure Account, Azure Copilot |
| 🐍 Python | Python, Pylance, Black Formatter |
| 🔧 DevOps | GitLens, GitHub PRs, Actions |

## 🖼️ What You'll See

When you open a terminal, you'll see the **Code to Cloud** ASCII art banner:

```
   ██████╗ ██████╗ ██████╗ ███████╗    ████████╗ ██████╗ 
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔═══██╗
  ██║     ██║   ██║██║  ██║█████╗         ██║   ██║   ██║
  ██║     ██║   ██║██║  ██║██╔══╝         ██║   ██║   ██║
  ╚██████╗╚██████╔╝██████╔╝███████╗       ██║   ╚██████╔╝
   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝ 

   ██████╗██╗      ██████╗ ██╗   ██╗██████╗ 
  ██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗
  ██║     ██║     ██║   ██║██║   ██║██║  ██║
  ██║     ██║     ██║   ██║██║   ██║██║  ██║
  ╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝
   ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ 

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🤖 Azure Agentic Engineering
  🚀 github.com/codetocloudorg
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔐 Authentication

After your Codespace starts:

```bash
# Azure CLI
az login --use-device-code

# Azure Developer CLI
azd auth login

# Verify
az account show
```

## 📊 Image Details

- **Base**: Ubuntu 24.04 LTS (Canonical Official)
- **Size**: ~1.8 GB
- **Security**: Non-root user, minimal attack surface

## 📂 File Structure

```
.devcontainer/
├── devcontainer.json   # Main Codespaces configuration
├── Dockerfile          # Container image definition
└── README.md           # This file
```

## 📖 Learn More

- [GitHub Codespaces Docs](https://docs.github.com/codespaces)
- [Dev Container Spec](https://containers.dev)
- [Code to Cloud Organization](https://github.com/codetocloudorg)
