# Contributing to Azure Agentic Engineering

Thank you for your interest in contributing to this repository! This guide will help you get started.

**This project is maintained by [Code to Cloud](https://github.com/codetocloudorg)**

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Documentation](#documentation)

## Code of Conduct

This project follows the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). By participating, you agree to abide by its terms.

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use the issue templates when available
- Provide detailed information:
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, Python/Node version, etc.)

### Suggesting Enhancements

- Open an issue with the "enhancement" label
- Describe the use case and expected benefit
- Include examples if possible

### Contributing Code

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Development Setup

### Prerequisites

```bash
# Required tools
- Git
- Python 3.10+
- Azure CLI
- Azure Developer CLI (azd)
```

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/azure-agentic-engineering.git
cd azure-agentic-engineering

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Environment Variables

Create a `.env` file (never commit this):

```bash
# Copy the example
cp .env.example .env

# Edit with your values
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
```

## Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Write docstrings for all public functions
- Maximum line length: 100 characters

```python
async def create_agent(
    name: str,
    instructions: str,
    tools: list[Callable] | None = None
) -> Agent:
    """
    Create a new AI agent.
    
    Args:
        name: The agent's name
        instructions: System instructions for the agent
        tools: Optional list of tool functions
        
    Returns:
        Configured Agent instance
        
    Raises:
        ValueError: If name is empty
    """
    ...
```

### Bicep/Terraform

- Use modules for reusable components
- Include descriptions for all parameters
- Follow naming conventions from the Azure Cloud Adoption Framework

### Documentation

- Use clear, concise language
- Include code examples
- Keep README files up to date

## Pull Request Process

### Before Submitting

1. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Run linting
   ruff check .
   mypy .
   ```

2. **Update documentation** if needed

3. **Ensure commits are clean**
   ```bash
   # Squash if needed
   git rebase -i main
   ```

### PR Requirements

- [ ] Clear title and description
- [ ] Links to related issues
- [ ] Tests for new functionality
- [ ] Documentation updates
- [ ] No secrets or credentials
- [ ] Passes CI checks

### PR Title Format

```
type(scope): description

Examples:
- feat(agents): add streaming support
- fix(docs): correct SDK installation instructions
- docs(security): add RBAC best practices
- chore(infra): update Bicep modules
```

### Review Process

1. A team member will review within 2-3 business days
2. Address any feedback
3. Once approved, a maintainer will merge

## Documentation

### Adding New Docs

- Place in appropriate `docs/` subdirectory
- Update navigation in README if needed
- Include practical examples

### Code Samples

- Must be runnable (or clearly marked as pseudocode)
- Include all necessary imports
- Add comments explaining key concepts

## Questions?

- Open a discussion in the repository
- Visit the [Code to Cloud organization](https://github.com/codetocloudorg)
- Check other projects in the org for related resources

Thank you for contributing! 🎉
