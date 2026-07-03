# CrewAI

**GitHub:** https://github.com/crewAIInc/crewAI
**Stars:** 54,805
**Topics:** agents, ai, ai-agents, aiagentframework, llms

## Overview
CrewAI is a standalone (not built on LangChain), production-oriented Python framework for multi-agent automation. It offers two complementary models: **Crews**, role-based agents that collaborate autonomously, and **Flows**, event-driven workflows for precise, deterministic control — including single LLM calls where a full agent isn't warranted.

## Problem It Solves
Pure autonomous multi-agent collaboration (Crews) is powerful but can be unpredictable for processes that need exact control points; pure deterministic pipelines can't adapt. CrewAI's Crews-and-Flows split lets a team mix both within one framework rather than choosing one paradigm for an entire system.

## Key Features / Use Cases
- **Crews** — role-based agents (role, goal, backstory, tools, memory, guardrails) that collaborate on open-ended tasks.
- **Flows** — event-driven orchestration combining precise control, single LLM calls, and native Crew invocation.
- **Structured task output** — `output_pydantic` / `output_json` for tasks that need machine-parseable results, plus human-review steps.
- **CrewAI AMP Suite** — an optional commercial control plane (tracing, governance, security) for teams running CrewAI in production.
- **Coding-agent skills** — official skills (`getting-started`, `design-agent`, `design-task`, `ask-docs`) that teach Claude Code/Cursor/Codex CrewAI's own patterns.

## Related
- [[microsoft__autogen]] — an actively-maintained alternative multi-agent framework, with a more conversation-centric (vs. role/crew-centric) mental model.
- [[langchain-ai__langchain]] — CrewAI is explicitly built independent of LangChain, a notable architectural distinction between the two.
