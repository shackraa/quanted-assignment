# RAGFlow

**GitHub:** https://github.com/infiniflow/ragflow
**Stars:** 84,178
**Topics:** agentic-ai, agentic-retrieval, ai-agents, context-engine, rag

## Overview
RAGFlow is a production-oriented, open-source Retrieval-Augmented Generation engine that combines deep document understanding with agent capabilities, aimed at turning messy enterprise documents into grounded, citation-backed answers.

## Problem It Solves
Naive RAG pipelines often fail on real-world documents — scanned PDFs, spreadsheets, slide decks, tables — and produce hallucinated or ungrounded answers. RAGFlow focuses on "quality in, quality out": deep document parsing, explainable chunking, and traceable citations so answers can be verified against source text.

## Key Features / Use Cases
- **Deep document understanding** — extracts structured knowledge from complex, heterogeneous file formats.
- **Grounded citations** — every answer traces back to visualized source chunks, reducing hallucination.
- **Agent templates + context engine** — pre-built agent workflows layered on top of the retrieval engine, plus a Python/JS code executor component.
- **Broad data source support** — Confluence, S3, Notion, Discord, Google Drive sync, MCP support.
- **Configurable models** — bring your own LLM and embedding model.

## Related
- [[langchain-ai__langchain]] — LangChain provides RAG as one of many composable primitives; RAGFlow is a full, opinionated product built around RAG + agents specifically.
