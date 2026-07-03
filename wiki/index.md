# AI Agent Ecosystem — Index

A knowledge vault covering popular GitHub repos in the AI-agent ecosystem: frameworks, orchestration/harnesses, memory, skills/plugins, agent tooling, and learning resources. Generated from READMEs in `raw/` and metadata in `manifest.json`.

## Frameworks

Full frameworks (or framework-adjacent products) for building single- or multi-agent LLM applications.

- [[langchain-ai__langchain]] — the widely-adopted agent/LLM application framework, with LangGraph and Deep Agents as companion layers.
- [[google-gemini__gemini-cli]] — Google's open-source terminal coding agent.
- [[infiniflow__ragflow]] — production RAG engine fused with agent capabilities and grounded citations.
- [[Mintplex-Labs__anything-llm]] — all-in-one, self-hostable document chat + agents + RAG application.
- [[microsoft__autogen]] — Microsoft's multi-agent framework, now in maintenance mode in favor of Microsoft Agent Framework.
- [[crewAIInc__crewAI]] — standalone multi-agent framework built around role-based Crews and event-driven Flows.

## Orchestration & Agent Harnesses

Projects that coordinate multiple agents, sub-agents, or swarms on top of a base coding agent.

- [[bytedance__deer-flow]] — ByteDance's "super agent harness" for long-horizon tasks via sub-agents, memory, and sandboxes.
- [[666ghj__MiroFish]] — multi-agent swarm simulation engine for prediction and scenario rehearsal.
- [[code-yeongyu__oh-my-openagent]] — orchestration/config layer for OpenCode and Codex CLI, model-agnostic by design.
- [[ruvnet__ruflo]] — agent meta-harness for Claude Code/Codex with swarms, learning, and federation.

## Memory

Persistent/long-term memory layers for agents.

- [[thedotmack__claude-mem]] — persistent memory compression built specifically for Claude Code.
- [[mem0ai__mem0]] — general-purpose, provider-agnostic memory layer for AI agents and assistants.
- [[letta-ai__letta]] — platform for building stateful agents around structured, agent-editable memory blocks, formerly known as MemGPT.

## Skills & Plugins

Skills, plugins, and reference catalogues for the Claude Code / agent-skill ecosystem.

- [[DietrichGebert__ponytail]] — a skill that curbs coding-agent over-engineering via a decision ladder.
- [[ComposioHQ__awesome-claude-skills]] — curated directory of 1000+ Claude Skills and plugins.
- [[shanraisshan__claude-code-best-practice]] — reference repo mapping Claude Code features to best practices and community workflows.

## Agent Tooling & Infrastructure

Tools that give agents access to external capabilities — the web, a browser, or a place to run code.

- [[firecrawl__firecrawl]] — API that converts web pages into clean, LLM-ready Markdown/JSON.
- [[browser-use__browser-use]] — gives agents a real, controllable browser instead of a scraping API.
- [[daytonaio__daytona]] — secure, fast-spinning-up sandbox infrastructure for AI-generated code execution (core development moved to a private codebase as of June 2026 — no further updates, but the repo remains open and usable).

## Learning Resources

Educational content on prompting and agent-building, not software.

- [[dair-ai__Prompt-Engineering-Guide]] — comprehensive prompt engineering technique reference and course.
- [[microsoft__ai-agents-for-beginners]] — Microsoft's structured, lesson-by-lesson course on building AI agents.
