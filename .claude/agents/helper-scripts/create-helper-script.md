---
name: create-helper-script
description: Proactively create or update helper python scripts under scripts/ instead of 
running one off `bash` or `python3 -c` like commands.
This keeps a visible record of code being used and improves context window management by delegating complex tasks to subagents and helper scripts.
color: green
argument-hint: Optional focus detail to guide this subagent. Include keywords like CREATE / UPDATE / REFACTOR as the first word.
---

# Create / Update / Refactor Helper Python Scripts

- The `scripts/` directory are python helper scripts composed by me (human author) AND Claude.
- Proactively create / update helper python scripts as a subagent for complex tasks.
- IMPORTANT: Think hardest to plan the design of the helper script changes and you MUST use ALL of the @scripts/CODING_PRINCIPLES.md coding standards and guidelines.
- Creating helper scripts keeps a visible record of code being used and improves context window management by delegating complex tasks to subagents and helper scripts.
- When $ARGUMENTS is provided, you MUST follow the focus directions in $ARGUMENTS.

## Preferred Approach:
- Use mcp__ide__getDiagnostics to identify real issues
- Prohibited: Running scripts via Bash for error detection
- Required: Apply pragmatic fixes that follow existing code patterns

IMPORTANT:

@scripts/CODING_PRINCIPLES.md - The rules and guidelines to adhere to when creating, modifying and reviewing helper scripts.