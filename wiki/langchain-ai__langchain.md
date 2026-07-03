# LangChain

**GitHub:** https://github.com/langchain-ai/langchain
**Stars:** 140,791
**Topics:** agents, ai, ai-agents, framework, langgraph, llm, rag

## Overview
LangChain is one of the original and most widely adopted frameworks for building agents and LLM-powered applications. It provides a standard interface across models, embeddings, vector stores, and tools, so an application isn't locked into one model provider's SDK.

## Problem It Solves
Building an LLM application from scratch means re-solving the same plumbing every time: swapping models, chaining calls, wiring in retrieval, handling tool calls. LangChain gives that plumbing a common set of abstractions, and lets teams change the underlying model or vector store without rewriting application logic.

## Key Features / Use Cases
- **Model interoperability** — one interface across OpenAI, Anthropic, Gemini, and others.
- **Component-based architecture** — chains, retrievers, and tools compose for rapid prototyping.
- **LangGraph** — a lower-level companion framework for controllable, stateful agent workflows, used when LangChain's higher-level abstractions aren't enough control.
- **Deep Agents** — a higher-level package on top of LangChain for agents with built-in planning, subagents, and filesystem use.
- **LangSmith** — observability, evals, and debugging for agents built on the framework.

## Related
- [[microsoft__autogen]] and [[crewAIInc__crewAI]] — alternative multi-agent orchestration frameworks with different philosophies (conversation-driven vs. role-based crews vs. LangChain's graph/chain composition).
- [[infiniflow__ragflow]] — a RAG-focused engine that plays a similar role to LangChain's retrieval components, but as a full standalone product.
