# Security Policy

## Reporting Security Vulnerabilities

We take the security of the IRC Chat Client seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Do not** open a public issue for security vulnerabilities. Instead:

1. Email security details to the project maintainers
2. Include a clear description of the vulnerability
3. Provide steps to reproduce the issue if possible
4. Allow time for a fix before public disclosure

### Security Best Practices

When using this IRC Chat Client:

- **Never share credentials** in public channels or logs
- **Use strong passwords** if the IRC server requires authentication
- **Keep dependencies updated** - Run `pip install -r requirements.txt --upgrade`
- **Run from trusted sources** - Only clone from trusted repositories
- **Review code** - Read the code before running unknown IRC client instances
- **Use HTTPS/TLS** when available - Some servers support secure connections
- **Protect config files** - Don't share `config.json` containing server credentials

### Supported Versions

- Latest version: Full security support
- Previous version: Security patches for 6 months
- Older versions: No guaranteed support

### Security Features

This project implements:

✓ Input validation and sanitization
✓ Thread-safe operations with locks
✓ Safe socket handling
✓ Error handling without information leakage
✓ No hardcoded credentials
✓ Secure configuration management

### Dependencies

We maintain a list of dependencies in `requirements.txt`. We recommend:

```bash
pip install -r requirements.txt --upgrade
```

### Disclosure Timeline

Upon receiving a vulnerability report:

1. We will acknowledge receipt within 48 hours
2. We will work on a fix immediately
3. We will release a patch version within 7 days (if critical)
4. We will credit the reporter (if desired)

### Questions?

For security questions, contact the project maintainers or open a discussion in the repository.
