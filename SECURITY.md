# Security Policy

## Reporting Security Issues

The [Code to Cloud](https://github.com/codetocloudorg) organization takes security seriously. We appreciate your efforts to responsibly disclose your findings.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

### Microsoft Security Response Center (MSRC)

Report vulnerabilities through the [Microsoft Security Response Center](https://msrc.microsoft.com/create-report).

### Email

You can also email security concerns to the team directly.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | ✅ Yes             |
| Older   | ❌ No              |

## Security Best Practices

When using this repository, follow these security practices:

### 1. Never Commit Secrets

- Use `.env` files for local development (in `.gitignore`)
- Use Azure Key Vault for production secrets
- Use Managed Identity instead of API keys

### 2. Use the Provided `.gitignore`

Our `.gitignore` is configured to prevent accidental commits of:
- `.env` files
- API keys and credentials
- Local configuration files
- Certificate files

### 3. Enable Security Features

When deploying to Azure:
- Enable private endpoints
- Use RBAC with least privilege
- Enable diagnostic logging
- Use Azure Defender for Cloud

### 4. Keep Dependencies Updated

- Regularly update SDK versions
- Monitor for security advisories
- Use Dependabot or similar tools

## Security Checklist

Before deploying any code from this repository:

- [ ] Verified no secrets in code or configuration
- [ ] Using `DefaultAzureCredential` for authentication
- [ ] Private endpoints configured for production
- [ ] RBAC roles follow least privilege principle
- [ ] Diagnostic logging enabled
- [ ] Content Safety measures in place

## Additional Resources

- [Azure Security Documentation](https://docs.microsoft.com/azure/security/)
- [Microsoft Security Response Center](https://msrc.microsoft.com/)
- [Azure Security Benchmark](https://docs.microsoft.com/security/benchmark/azure/)
