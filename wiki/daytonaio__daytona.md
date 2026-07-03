# Daytona

**GitHub:** https://github.com/daytonaio/daytona
**Stars:** 72,322
**Topics:** agentic-workflow, ai, ai-runtime, ai-sandboxes, code-execution

## Overview
Daytona is secure, elastic sandbox infrastructure for running AI-generated code — full isolated "composable computers" (dedicated kernel, filesystem, network, CPU/RAM) that spin up in under 90ms. Note: per the project's own README, as of June 2026 Daytona's core development has moved to a private codebase, and this public repo will receive no further updates, fixes, or releases — but it remains open (not GitHub-archived/read-only) and usable as-is.

## Problem It Solves
Agents that write and execute code need somewhere safe to run it — isolated from the host system, reproducible, and fast enough to spin up per-task without becoming the bottleneck. Daytona is infrastructure purpose-built for that, rather than a general container platform repurposed for agents.

## Key Features / Use Cases
- **Sandboxes** — full isolated environments with persistent, stateful snapshots across sessions.
- **Agent tools** — programmatic process/code execution, filesystem operations, computer use, MCP server.
- **Multi-language SDKs** — Python, TypeScript, Ruby, Go, Java clients for driving sandboxes from application code.
- **Platform/governance layer** — organizations, API keys, audit logs for teams standardizing on it.

## Related
- [[bytedance__deer-flow]] — DeerFlow's "sandbox mode" solves the same underlying problem (safe code execution for agents) as an integrated feature rather than standalone infrastructure.
