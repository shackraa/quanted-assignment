# AutoGen

**GitHub:** https://github.com/microsoft/autogen
**Stars:** 59,448
**Topics:** agentic, agents, autogen, framework, llm-agent, llm-framework

## Overview
AutoGen is Microsoft's framework for building multi-agent AI applications where agents act autonomously or alongside humans. It's now in **maintenance mode** — Microsoft's recommended successor for new projects is Microsoft Agent Framework, with a published migration guide for existing AutoGen users.

## Problem It Solves
Coordinating multiple specialized agents (a math expert, a chemistry expert, a general assistant that delegates to both) requires an orchestration layer above single-agent chat loops. AutoGen popularized patterns for that — `AssistantAgent`, `AgentTool`, and MCP-based tool workbenches — that later frameworks built on.

## Key Features / Use Cases
- **AgentChat** — the core API for defining assistant agents with system messages, tools, and streaming.
- **MCP workbenches** — agents can use external MCP servers (e.g. Playwright for browsing) as tool sources.
- **Agent-as-tool composition** — wrap one agent (`AgentTool`) so another agent can call it like any other tool, enabling simple multi-agent orchestration without a heavier framework.
- **AutoGen Studio** — a no-code GUI for building agent workflows.

## Related
- [[langchain-ai__langchain]] and [[crewAIInc__crewAI]] — comparable multi-agent frameworks; unlike AutoGen, both are under active development, a relevant distinction now that AutoGen itself is in maintenance mode.
