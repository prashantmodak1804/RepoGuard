# User Stories
## P1: Dependency Manifest Parsing
As a user, I want the license compliance agent to parse the dependency manifest files (`package.json`, `requirements.txt`) so that I can verify the licenses of the dependencies.

## P2: Policy Matching
As a user, I want the license compliance agent to match the licenses of the dependencies against the policy defined in `policy.json` so that I can ensure compliance with the project safety guidelines.

## P3: Citation Generation
As a user, I want the license compliance agent to generate citations for the licenses of the dependencies so that I can properly document the licenses used in the project.

## Edge Cases
* Malformed lines in the dependency manifest files
* Unknown licenses in the dependency manifest files
* Missing files in the dependency manifest files