# =============================================================================
# Azure Agentic Engineering - Ultra-Lean Secure Container
# Code to Cloud | github.com/codetocloudorg
#
# Base: Ubuntu 24.04 LTS (Canonical Official)
# Security: Minimal attack surface, reputable vendor
# =============================================================================

FROM ubuntu:24.04 AS base

# Avoid prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Reduce .NET telemetry
    DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_NOLOGO=1

LABEL maintainer="Code to Cloud <github.com/codetocloudorg>" \
    description="Azure AI & Agentic Engineering - Ultra-Lean" \
    version="2.0.0" \
    base-image="ubuntu:24.04-minimal"

# =============================================================================
# Minimal System Dependencies
# =============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Essentials only
    ca-certificates \
    curl \
    wget \
    git \
    gnupg \
    # Python runtime (no full dev tools)
    python3-minimal \
    python3-pip \
    python3-venv \
    # ICU for .NET
    libicu74 \
    # Shell
    bash \
    # Cleanup immediately
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && apt-get clean

# =============================================================================
# Create non-root user (security best practice)
# =============================================================================
RUN getent passwd 1000 > /dev/null && userdel -r $(getent passwd 1000 | cut -d: -f1) || true \
    && useradd -m -s /bin/bash -u 1000 vscode \
    && mkdir -p /home/vscode/.azure /home/vscode/.local/bin \
    && chown -R vscode:vscode /home/vscode

# =============================================================================
# Azure CLI (minimal install via pip - smaller than apt package)
# =============================================================================
RUN pip3 install --no-cache-dir --break-system-packages azure-cli \
    && az extension add --name resource-graph --yes 2>/dev/null || true \
    && rm -rf /root/.cache/pip

# =============================================================================
# Azure Developer CLI (azd)
# =============================================================================
RUN curl -fsSL https://aka.ms/install-azd.sh | bash \
    && rm -rf /tmp/*

# =============================================================================
# GitHub CLI
# =============================================================================
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Python AI Packages (core only - user can add more)
# =============================================================================
RUN pip3 install --no-cache-dir --break-system-packages \
    azure-identity \
    azure-ai-projects \
    azure-ai-inference \
    openai \
    agent-framework --pre \
    python-dotenv \
    && rm -rf /root/.cache/pip

# =============================================================================
# Switch to non-root user
# =============================================================================
USER vscode
WORKDIR /home/vscode
ENV PATH="/home/vscode/.local/bin:$PATH"

# =============================================================================
# MOTD (Code to Cloud branding)
# =============================================================================
RUN cat > ~/.local/bin/motd.sh << 'EOF'
#!/bin/bash
echo ""
echo -e "\033[0;36m   ██████╗ ██████╗ ██████╗ ███████╗    ████████╗ ██████╗ \033[0m"
echo -e "\033[0;36m  ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔═══██╗\033[0m"
echo -e "\033[0;34m  ██║     ██║   ██║██║  ██║█████╗         ██║   ██║   ██║\033[0m"
echo -e "\033[0;34m  ██║     ██║   ██║██║  ██║██╔══╝         ██║   ██║   ██║\033[0m"
echo -e "\033[0;35m  ╚██████╗╚██████╔╝██████╔╝███████╗       ██║   ╚██████╔╝\033[0m"
echo -e "\033[0;35m   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝ \033[0m"
echo ""
echo -e "\033[0;36m   ██████╗██╗      ██████╗ ██╗   ██╗██████╗ \033[0m"
echo -e "\033[0;36m  ██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗\033[0m"
echo -e "\033[0;34m  ██║     ██║     ██║   ██║██║   ██║██║  ██║\033[0m"
echo -e "\033[0;34m  ██║     ██║     ██║   ██║██║   ██║██║  ██║\033[0m"
echo -e "\033[0;35m  ╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝\033[0m"
echo -e "\033[0;35m   ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ \033[0m"
echo ""
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  \033[0;32m🤖 Azure Agentic Engineering\033[0m"
echo -e "  \033[0;33m🚀 github.com/codetocloudorg\033[0m"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
PY_VER=$(python3 --version 2>/dev/null | cut -d' ' -f2)
AZ_VER=$(az version 2>/dev/null | grep -o '"azure-cli": "[^"]*"' | cut -d'"' -f4)
AZD_VER=$(azd version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
GH_VER=$(gh --version 2>/dev/null | head -1 | cut -d' ' -f3)
echo "  📦 Python    ${PY_VER:-not installed}"
echo "  ☁️  Azure CLI ${AZ_VER:-not installed}"
echo "  🚀 AZD       ${AZD_VER:-not installed}"
echo "  🐙 GitHub    ${GH_VER:-not installed}"
echo ""
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  \033[0;32mQuick Start:\033[0m"
echo "    az login --use-device-code"
echo "    azd auth login"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
EOF
RUN chmod +x ~/.local/bin/motd.sh \
    && echo 'if [ -f ~/.local/bin/motd.sh ]; then ~/.local/bin/motd.sh; fi' >> ~/.bashrc

WORKDIR /workspaces
CMD ["/bin/bash"]
