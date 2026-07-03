# Mem0

**GitHub:** https://github.com/mem0ai/mem0
**Stars:** 59,983
**Topics:** agents, ai-agents, chatbots, llm, long-term-memory, memory-management, rag

## Overview
Mem0 ("mem-zero") is a general-purpose intelligent memory layer for AI assistants and agents: it remembers user preferences and facts, and continuously updates that memory across sessions instead of restarting from a blank context every time.

## Problem It Solves
LLM applications are stateless between calls by default. Building durable personalization (a customer support bot that remembers a user's past tickets, an assistant that adapts to a user's preferences) otherwise means hand-rolling storage, retrieval, and update logic — Mem0 packages that as a memory algorithm plus API.

## Key Features / Use Cases
- **Multi-level memory** — User, Session, and Agent-scoped memory in one model.
- **Single-pass ADD-only extraction** — one LLM call per memory update, no destructive overwrite, which the project's own benchmarks show meaningfully improves recall accuracy (LoCoMo, LongMemEval) over their previous UPDATE/DELETE approach.
- **Multi-signal retrieval** — semantic, BM25 keyword, and entity matching fused together, plus temporal reasoning for "what was true when" queries.
- **Three deployment tiers** — a pip/npm library for prototyping, a self-hosted server for teams, or a managed cloud platform.
- **Agent-first signup** — agents can mint their own API key programmatically (no human email/OTP step) so an autonomous agent can start using memory without a human provisioning it first.

## Related
- [[thedotmack__claude-mem]] — a Claude-Code-specific memory system in the same space.
- [[Mintplex-Labs__anything-llm]] — uses memory as one feature of a broader application rather than as the core product.
