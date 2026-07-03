# Gemini CLI

**GitHub:** https://github.com/google-gemini/gemini-cli
**Stars:** 105,721
**Topics:** ai, ai-agents, cli, gemini, mcp-client, mcp-server

## Overview
Gemini CLI is Google's open-source terminal agent — a direct, lightweight way to bring Gemini models into a developer's command line for code understanding, generation, and automation, comparable in spirit to Claude Code or Codex CLI.

## Problem It Solves
Developers who live in the terminal don't want to context-switch to a chat UI to get AI help with their codebase. Gemini CLI puts a capable coding agent directly where the work happens, with a generous free tier (60 requests/min, 1M-token context) that lowers the barrier to trying it.

## Key Features / Use Cases
- **Code understanding & generation** — query/edit large codebases, generate apps from images or sketches, debug via natural language.
- **Built-in tools** — Google Search grounding, file operations, shell commands.
- **MCP support** — extensible with Model Context Protocol servers for custom capabilities (e.g. image/video generation).
- **GitHub integration** — automated PR reviews and issue triage via a companion GitHub Action.
- **Non-interactive mode** — scriptable for CI/workflow automation, not just interactive chat.

## Related
- [[thedotmack__claude-mem]] — claude-mem explicitly supports installing into Gemini CLI's config directory, showing these terminal agents share plugin/memory ecosystems.
