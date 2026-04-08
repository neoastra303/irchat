# IRChat Documentation

Comprehensive guides, specifications, and references for the IRChat project.

## Quick Navigation

### 📖 Getting Started
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical design, threading model, and system architecture
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards and code of conduct

### 🔒 Security & Compliance
- **[SECURITY.md](SECURITY.md)** - Security policy, vulnerability reporting, and best practices
- **[SECURITY_AUDIT.md](SECURITY_AUDIT.md)** - Detailed security audit and findings

### 📝 Project Information
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[PRESENTATION.md](PRESENTATION.md)** - Project overview, vision, use cases, and bot examples
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation index

### 📦 Deployment & Status
See the [status/](status/) folder for deployment checklists and setup guides:
- `AUTOMATION_COMPLETE.txt` - GitHub automation setup summary
- `DEPLOYMENT_CHECKLIST.md` - Steps for production deployment
- `GIT_SETUP_COMPLETE.txt` - Git initialization status
- `GITHUB_SETUP.md` - GitHub repository setup guide
- `GITHUB_PUSH_GUIDE.md` - Instructions for pushing code to GitHub

## Document Overview

| Document | Purpose | Audience |
|----------|---------|----------|
| ARCHITECTURE.md | Technical design & implementation details | Developers |
| CONTRIBUTING.md | Development guidelines & workflow | Contributors |
| CODE_OF_CONDUCT.md | Community standards & behavior | Everyone |
| SECURITY.md | Vulnerability reporting & security practices | Everyone |
| SECURITY_AUDIT.md | Detailed security findings | Developers |
| CHANGELOG.md | Version history & release notes | Everyone |
| PRESENTATION.md | Project overview & vision | Decision makers |
| DOCUMENTATION_INDEX.md | Master index of all docs | Everyone |

## Key Features Documented

### Architecture
- **RFC 2812 Compliance**: Full IRC protocol implementation
- **Thread Safety**: Lock-based synchronization with Event-based registration
- **Non-blocking I/O**: select.select() for responsive UI
- **Security**: Input validation, sanitization, no hardcoded credentials

### Community
- Professional code of conduct
- Clear contribution guidelines
- Structured issue templates
- Pull request requirements

### Security
- Vulnerability disclosure policy
- Input validation constraints (nick 30 chars, channel 50 chars, message 400 chars)
- No control characters in input
- Configuration file security (git-ignored)
- Dependency scanning (Dependabot, CodeQL)

## For Different Audiences

### 👨‍💻 Developers
1. Start with **ARCHITECTURE.md** - understand the design
2. Read **CONTRIBUTING.md** - learn the workflow
3. Check **SECURITY.md** - understand security practices
4. Review **CHANGELOG.md** - see what's been built

### 🤝 Contributors
1. Review **CODE_OF_CONDUCT.md** - community standards
2. Read **CONTRIBUTING.md** - contribution process
3. Check **SECURITY.md** - security guidelines
4. Submit PRs following the guidelines

### 🔐 Security Researchers
1. Start with **SECURITY.md** - vulnerability reporting
2. Review **SECURITY_AUDIT.md** - known findings
3. Check **ARCHITECTURE.md** - implementation details
4. Report issues via GitHub security advisories

### 📊 Project Managers
1. Review **PRESENTATION.md** - project overview
2. Check **CHANGELOG.md** - progress and versions
3. See status/ folder - deployment progress
4. Review **DOCUMENTATION_INDEX.md** - complete picture

## Contributing to Documentation

All documentation files are in this folder. When making changes:

1. **Keep it clear**: Write for your intended audience
2. **Keep it current**: Update docs when code changes
3. **Use markdown**: All docs are .md files
4. **Structure it**: Use headers, lists, and tables
5. **Link it**: Cross-reference related docs

## Build & Deployment

For deployment information, see the [status/](status/) folder:
- Complete deployment checklists
- GitHub automation setup
- Git workflow guides
- Release procedures

## Questions or Feedback?

- Check **DOCUMENTATION_INDEX.md** for what you're looking for
- Review **CODE_OF_CONDUCT.md** for community guidelines
- Open an issue following the template in `.github/ISSUE_TEMPLATE/`
