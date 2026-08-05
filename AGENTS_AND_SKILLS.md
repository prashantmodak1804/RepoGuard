# Custom Agents and Skills Specification
## Custom Agent: LicenseComplianceAgent
- **Role**: Analyzes target project dependencies and verifies whether open-source licenses comply with project safety guidelines.
- **Responsibilities**:
  - Ingest normalized package dependency lists.
  - Detect non-compliant copyleft licenses (e.g., GPL-3.0, AGPL-3.0).
  - Output verifiable audit reports with grounded citations for every flagged item.
- **Rules**: Must refuse to generate unverified claims without direct citations to rule lines or official license terms.

## Custom Skill: ManifestParserSkill
- **Role**: Extracts raw package identifiers and version strings from standard project manifests.
- **Supported Formats**: `package.json`, `requirements.txt`.
- **Input**: File path or raw manifest content string.
- **Output**: Standardized JSON array containing objects structured as `{ "package": string, "version": string, "manifest_type": string }`.

## Custom Skill: PolicySkill
- **Role**: Checks the compliance of given packages against the policy defined in the policy.json file.
- **Supported Formats**: JSON policy files.
- **Input**: File path or raw policy content string.
- **Output**: A list of dictionaries containing the compliance status of each package.