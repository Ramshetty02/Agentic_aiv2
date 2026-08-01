# Security Policy

## Supported Versions

Security fixes target the default branch until tagged releases exist.

## Reporting a Vulnerability

Open a private GitHub security advisory or contact the repository owner directly through GitHub.

Do not include API keys, private prompts, private research data, or user secrets in public issues.

## Data Handling

EREVNA stores local research memory in `database/` and run logs in `logs/`. Both paths are ignored by git. Treat saved reports and queries as user data and delete those folders when a machine or deployment is handed off.

## Network Fetching

The web retriever must reject unsafe URL schemes and private network targets before scraping. Any future connector that fetches remote content needs the same boundary.

