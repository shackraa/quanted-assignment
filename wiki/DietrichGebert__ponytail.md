# Ponytail

**GitHub:** https://github.com/DietrichGebert/ponytail
**Stars:** 71,985
**Topics:** agent-skills, ai-agents, claude-code, claude-code-plugin, cursor-rules

## Overview
Ponytail is a Claude Code / Codex / Copilot CLI skill and plugin that pushes coding agents toward minimal, non-over-engineered output — modeled on "the laziest senior dev in the room" who replaces fifty lines with one.

## Problem It Solves
Left alone, coding agents tend to over-build: installing a dependency and writing a wrapper component for something a single native HTML attribute would solve. Ponytail installs a decision ladder the agent runs through before writing code, cutting unnecessary code without cutting validation, security, or accessibility.

## Key Features / Use Cases
- **Decision ladder** — does this need to exist? already in the codebase? stdlib? native platform feature? installed dependency? one line? only then, the minimum that works.
- **Multi-agent support** — works across Claude Code, Codex, GitHub Copilot CLI, Pi, OpenCode, Gemini CLI, and Antigravity via each platform's plugin/extension system.
- **Benchmarked** — published, reproducible benchmarks (agentic sessions on a real FastAPI+React repo) showing measurable reductions in LOC, tokens, cost, and time versus a no-skill baseline, while holding safety constant.
- **Command levels** — lite/full/ultra/off levels for how aggressively the ruleset is enforced.

## Related
- [[ComposioHQ__awesome-claude-skills]] — a directory that this kind of skill would typically be catalogued in.
