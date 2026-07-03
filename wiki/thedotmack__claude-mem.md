# Claude-Mem

**GitHub:** https://github.com/thedotmack/claude-mem
**Stars:** 85,578
**Topics:** ai-agents, ai-memory, claude, claude-code-plugin, long-term-memory, mem0, rag

## Overview
Claude-Mem is a persistent memory compression system built specifically for Claude Code (with support for Gemini CLI and OpenClaw). It automatically captures what an agent does during a session, compresses it into semantic summaries, and re-injects that context into future sessions.

## Problem It Solves
Coding agent sessions are stateless by default — context about a project, past decisions, or prior debugging is lost the moment a session ends. Claude-Mem solves this without requiring the user to manually re-explain project history every time.

## Key Features / Use Cases
- **Automatic capture** — hooks into tool usage during a session, no manual note-taking required.
- **Progressive disclosure** — layered memory retrieval with visibility into token cost, so recall doesn't silently blow up context.
- **Skill-based search** — query project history in natural language via a dedicated search skill.
- **Web viewer** — a local real-time UI for browsing the memory stream.
- **Privacy controls** — `<private>` tags exclude sensitive content from storage.

## Related
- [[mem0ai__mem0]] — a more general-purpose memory layer not tied to Claude Code specifically; Claude-Mem's own README lists it as a related engine in the same space.
