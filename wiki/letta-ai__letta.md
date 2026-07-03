# Letta (formerly MemGPT)

**GitHub:** https://github.com/letta-ai/letta
**Stars:** 23,624
**Topics:** ai-agents, llm, memory, agents

## Overview
Letta (the project formerly known as MemGPT) is a platform for building **stateful agents** — agents with advanced memory that persists and improves over time, rather than resetting with every new conversation. It ships both as a CLI (Letta Code, for running memory-equipped agents locally in a terminal) and as a full agents API with Python/TypeScript SDKs for embedding stateful agents into applications.

## Problem It Solves
Most agent frameworks treat memory as an add-on bolted onto a stateless chat loop. Letta builds the agent around memory from the start — structured memory blocks the agent can read and edit about itself and the user, so an agent can accumulate and refine what it knows about a person or task across sessions, not just within one.

## Key Features / Use Cases
- **Letta Code** — a terminal CLI (`npm install -g @letta-ai/letta-code`) that runs a memory-equipped coding/task agent locally, with bundled skills and subagents for continual learning.
- **Structured memory blocks** — agents are created with explicit, labeled memory (e.g. a `human` block and a `persona` block) that the agent can read and update, rather than an opaque memory store.
- **Full agents API** — Python and TypeScript SDKs for creating and messaging stateful agents from application code.
- **Model-agnostic** — works with any underlying LLM; the project publishes its own model leaderboard for which models perform best as the reasoning engine behind a Letta agent.

## Related
- [[mem0ai__mem0]] — another dedicated memory-layer project; Letta builds memory into the agent itself (memory blocks as part of agent state) versus Mem0's approach of a separate memory service agents call into.
- [[thedotmack__claude-mem]] — a narrower, Claude-Code-specific take on the same persistent-memory problem.
