# Oh My OpenAgent (OmO)

**GitHub:** https://github.com/code-yeongyu/oh-my-openagent
**Stars:** 64,633
**Topics:** ai-agents, claude-skills, codex, opencode, orchestration

## Overview
Oh My OpenAgent (OmO) is a configuration/orchestration layer for OpenCode and Codex CLI — agent definitions, lifecycle hooks, MCP integrations, and slash commands bundled so a coding agent can run multiple models and providers in a coordinated way ("Team Mode") instead of being locked to one vendor's CLI.

## Problem It Solves
Developers juggling Claude Code, Codex, and assorted open models end up re-solving the same configuration and orchestration problems per tool. OmO packages that setup once, across two editions sized for different platforms.

## Key Features / Use Cases
- **Ultimate Edition (OpenCode)** — 11 agents, 50+ lifecycle hooks, 5 built-in MCPs, full orchestration ("Team Mode"), an autonomous work loop (`ultrawork`).
- **Light Edition (Codex CLI)** — a portable subset (rules, LSP, git-bash, telemetry) that fits Codex's plugin system without full agent orchestration.
- **Model-agnostic philosophy** — explicitly built around not depending on a single provider as models get cheaper and more capable across the board.
- **LLM-guided install** — the setup is complex enough that the README recommends letting an agent read the install guide and configure itself.

## Related
- [[ruvnet__ruflo]] and [[bytedance__deer-flow]] — comparable "harness" projects layering orchestration, multi-agent coordination, and memory on top of a base coding agent.
