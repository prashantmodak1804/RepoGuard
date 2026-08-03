# RepoGuardian — Architecture & Design Specification

## 1. Executive Summary
RepoGuardian is an agent-driven compliance and security auditing system built for software development teams. It inspects software project dependency manifests (e.g., `package.json`, `requirements.txt`), evaluates them against defined organizational compliance policies (e.g., restricted open-source licenses, vulnerable dependencies), and generates structured, audit-ready compliance reports backed by verifiable citations.

## 2. Technical Stack
- **CLI & Application Core**: Python 3.11+ (utilizing `typer` for CLI routing and `rich` for formatted terminal output)
- **Specification Framework**: GitHub Spec Kit (`specify-cli`)
- **Agent Workflow**: VS Code + Cline / Roo Code (Human-in-the-Loop review model)
- **LLM Backends**:
  - **Plan Mode**: Google Gemini Flash (Architectural reasoning, task planning, and spec generation)
  - **Act Mode**: NVIDIA Build API (`meta/llama-3.3-70b-instruct` / `glm-5.2`) for code execution and file generation
- **CI/CD & Automated Verification**: GitHub Actions, PyTest, Playwright

## 3. High-Level Data Flow
1. **Ingestion**: `ManifestParserSkill` reads and normalizes raw dependency files (`package.json` or `requirements.txt`).
2. **Policy Matching**: `LicenseComplianceAgent` cross-references package licenses against defined rules in `policy.json`.
3. **Citation & Verification Engine**: LLM agent evaluates license terms and appends explicit citations pointing to specific policy rule lines or official OSI license terms.
4. **Report Output**: Outputs a color-coded terminal summary table and generates a markdown report (`AUDIT_REPORT.md`).