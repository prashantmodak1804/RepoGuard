# RepoGuardian

**RepoGuardian** is a lightweight license-compliance auditor for software projects. It parses your project's dependency manifest, looks up each package's license, checks it against your organization's license policy, and produces a citation-backed compliance report — all from the command line.

Every result RepoGuardian produces is traceable back to a specific rule or a specific missing entry — no unexplained "pass" or "fail," just grounded citations like:
> `license 'MIT' matches the 'allowed' list in policy.json`

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Custom Agents & Skills](#custom-agents--skills)
- [Models Used](#models-used)
- [Tools & Workflows Used](#tools--workflows-used)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Manifest parsing** for `package.json` (npm, including both `dependencies` and `devDependencies`) and `requirements.txt` (pip).
- **Policy-based compliance checking** against a configurable `allowed` / `warning` / `denied` license list.
- **Grounded citations** for every result — each status is backed by an explicit reference to the policy rule or the missing license-database entry that produced it.
- **CLI-first workflow** via [Typer](https://typer.tiangolo.com/), with a readable [Rich](https://rich.readthedocs.io/)-rendered table in the terminal.
- **Markdown audit report** (`AUDIT_REPORT.md`) generated automatically on every run.
- **CI-friendly exit codes** — the CLI exits non-zero if any package resolves to a `denied` license, so it can gate a pipeline.

---

## How It Works

```
 manifest file            license database          policy file
(package.json /    ─┐    (license_db.json)   ─┐    (policy.json)
 requirements.txt)   │                          │
        │            │                          │
        ▼            ▼                          ▼
  manifest_parser.py ──► license_agent.py ──► compliance results
        │                                         │
        ▼                                         ▼
  [{package, version,                    [{package, version, license,
    manifest_type}]                        status, citation}]
                                                    │
                                                    ▼
                                         Rich table (stdout)
                                         + AUDIT_REPORT.md
```

1. **`manifest_parser.py`** reads a manifest file and normalizes it into a flat list of `{package, version, manifest_type}` entries.
2. **`license_agent.py`** looks up each package's license in `license_db.json`, checks it against `policy.json`'s `allowed` / `warning` / `denied` lists, and attaches a human-readable citation to every result.
3. **`main.py`** ties it together as a CLI command, prints a formatted table, and writes `AUDIT_REPORT.md`.

---

## Installation

Requires Python 3.11+.

```bash
# Clone the repo
git clone <https://github.com/prashantmodak1804/RepoGuard>
cd <RepoGuard>

# Install runtime dependencies
pip install -r requirements.txt

# (Optional) Install dev dependencies — linting, testing, browser-based e2e tests
pip install -r requirements-dev.txt
python -m playwright install --with-deps chromium
```

---

## Usage

Run an audit against any supported manifest file:

```bash
python main.py audit examples/package.json
```

This prints a compliance table to the terminal and writes a full report to `AUDIT_REPORT.md`.

Check the tool's version:

```bash
python main.py version
```

**Exit codes:**
| Code | Meaning |
|---|---|
| `0` | Audit completed, no `denied` licenses found |
| `1` | At least one package resolved to a `denied` license, **or** the manifest couldn't be read |

This makes `main.py audit` safe to drop straight into a CI pipeline as a gate.

---

## Configuration

RepoGuardian is configured through two JSON files at the repo root:

### `policy.json`
Defines which licenses are acceptable:

```json
{
  "denied": ["GPL-3.0", "AGPL-3.0"],
  "warning": ["LGPL-3.0"],
  "allowed": ["MIT", "Apache-2.0", "BSD-3-Clause"]
}
```

### `license_db.json`
Maps package names to their known license:

```json
{
  "react": "MIT",
  "django": "BSD-3-Clause"
}
```

If a package isn't found in `license_db.json`, it's marked `unknown` with a citation explaining exactly why (no silent failures).

> Edit both files to match your organization's actual policy and dependency licenses — the versions checked into this repo are sample/demo data.

---

## Project Structure

```
.
├── main.py                  # CLI entrypoint (Typer)
├── manifest_parser.py       # Parses package.json / requirements.txt
├── license_agent.py         # Compliance checking against policy.json
├── policy.json               # License policy (allowed/warning/denied)
├── license_db.json           # Known package → license mapping
├── examples/
│   └── package.json          # Sample manifest for demos/CI smoke test
├── tests/
│   ├── test_manifest_parser.py
│   ├── test_license_agent.py
│   └── test_e2e_playwright.py
├── specs/                    # Spec-driven-development artifacts (see below)
├── .github/workflows/ci.yml  # CI pipeline definition
├── ARCHITECTURE.md           # CI/CD pipeline overview
├── CONSTITUTION.md           # Citation format rules
└── AGENTS_AND_SKILLS.md      # Custom agent/skill specifications
```

---

## Testing

The test suite covers manifest parsing, compliance logic, and an end-to-end browser check:

```bash
python -m pytest -v
```

| Test file | Covers |
|---|---|
| `tests/test_manifest_parser.py` | `package.json` and `requirements.txt` parsing, malformed-line handling |
| `tests/test_license_agent.py` | Allowed / denied / unknown compliance paths and citation correctness |
| `tests/test_e2e_playwright.py` | End-to-end CLI/report behavior via Playwright |

Lint the codebase with [Ruff](https://docs.astral.sh/ruff/):

```bash
ruff check .
```

---

## CI/CD

Every push to `main` triggers the pipeline defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml):

1. Checkout code
2. Set up Python 3.11
3. Install `requirements.txt` + `requirements-dev.txt`, install Playwright's Chromium browser
4. `ruff check .`
5. `python -m pytest`
6. Smoke test: `python main.py audit examples/package.json`

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for more detail.

---

## Custom Agents & Skills

This project was built using a spec-driven development workflow with custom-defined agents and skills — see [`AGENTS_AND_SKILLS.md`](AGENTS_AND_SKILLS.md) for full definitions. Summary:

- **`LicenseComplianceAgent`** — analyzes dependency lists, flags non-compliant copyleft licenses, and produces citation-grounded audit output.
- **`ManifestParserSkill`** — extracts package identifiers/versions from `package.json` and `requirements.txt`.
- **`PolicySkill`** — checks package compliance against `policy.json`.

Citation formatting rules for all compliance output are governed by [`CONSTITUTION.md`](CONSTITUTION.md).

The `specs/001-license-compliance-agent/` directory contains the original spec, plan, and task breakdown this project was implemented from.

---

## Models Used

<!--
  This project was built with AI assistance. List the specific model(s)/versions used
  at each stage below — e.g. spec writing, implementation, debugging, code review.
  Add rows as needed.
-->

| Stage | Model | Notes |
|---|---|---|
| Spec / planning | meta/llama-3.3-70b-instruct | |
| Implementation | meta/llama-3.3-70b-instruct | |
| Debugging / fixes | meta/llama-3.3-70b-instruct | |
| Code review | claude.ai | |

---

## Tools & Workflows Used

<!--
  Similarly, list any other tools, agents, or workflows involved in building this repo
  (e.g. coding agents, CI services, spec-kit tooling) that aren't captured above.
-->

- _add tool/workflow_
- _add tool/workflow_

---

## Contributing

<!-- Add contribution guidelines here if this project accepts external contributions. -->

1. Fork the repo and create a feature branch.
2. Make your changes with test coverage.
3. Ensure `ruff check .` and `python -m pytest` both pass locally.
4. Open a pull request.

---

## License

<!-- Add the project's license here (e.g. MIT, Apache-2.0) — no LICENSE file currently exists in this repo. -->

_Not yet specified._
