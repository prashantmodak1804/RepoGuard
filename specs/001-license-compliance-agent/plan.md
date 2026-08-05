# Technical Architecture
The license compliance agent will consist of the following components:
* Dependency manifest parser
* Policy matcher
* Citation generator

# CLI Input/Output Interfaces
The license compliance agent will use the following CLI input/output interfaces:
* Input: `package.json`, `requirements.txt`, `policy.json`
* Output: Citation reports

# Schema for policy.json and license_db.json
The `policy.json` file will contain the following schema:
* `allowed`: list of allowed licenses
* `warning`: list of warning licenses
* `denied`: list of denied licenses

The `license_db.json` file will contain the following schema:
* `licenses`: dictionary of licenses with their corresponding citations

# Verification Plan
The license compliance agent will use the following verification plan:
* Parse the dependency manifest files
* Match the licenses of the dependencies against the policy
* Generate citations for the licenses of the dependencies