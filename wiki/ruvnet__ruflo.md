# Ruflo (formerly Claude Flow)

**GitHub:** https://github.com/ruvnet/ruflo
**Stars:** 62,699
**Topics:** agentic-framework, ai-agents, multi-agent, multi-agent-systems, swarm

## Overview
Ruflo is an agent meta-harness for Claude Code and Codex: it adds 100+ specialized agents, coordinated swarms, self-learning memory, and cross-machine federation on top of the base coding agent, aiming to give it "a nervous system" rather than replace it.

## Problem It Solves
A single coding agent session doesn't self-organize into specialized roles, doesn't persist learning across tasks, and can't coordinate with agents running on other machines. Ruflo's router/swarm/memory/learning-loop architecture targets exactly that gap.

## Key Features / Use Cases
- **Two install paths** — a lightweight Claude Code plugin (slash commands only) vs. a full CLI install (`npx ruflo init`) that registers an MCP server, hooks, and daemon.
- **35 plugins** across orchestration, memory/knowledge (vector DB, RAG-memory, knowledge graphs), intelligence/learning, code quality, security, architecture methodology, and DevOps/observability.
- **Self-learning loop** — agents are meant to learn from successful task patterns and get more efficient over time.
- **Federation** — agents on different machines can collaborate securely without a central data leak point.

## Related
- [[code-yeongyu__oh-my-openagent]] and [[bytedance__deer-flow]] — overlapping "meta-harness" category; each takes a different architectural bet on orchestration and memory.
