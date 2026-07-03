# Firecrawl

**GitHub:** https://github.com/firecrawl/firecrawl
**Stars:** 143,370
**Topics:** ai, ai-agents, ai-crawler, ai-scraping, web-crawler, web-scraping, llm

## Overview
Firecrawl is an API that turns arbitrary web pages into clean, LLM-ready data — Markdown, structured JSON, or screenshots — instead of raw, noisy HTML. It's built specifically for feeding agents: rotating proxies, JS rendering, rate-limit handling, and PDF/DOCX parsing are handled server-side so an agent (or the developer building one) doesn't have to.

## Problem It Solves
Agents that need live web information (search results, documentation, product pages) hit the same wall every time: pages are JS-heavy, blocked by anti-bot measures, or return bloated HTML that burns tokens. Firecrawl abstracts that away behind a handful of endpoints.

## Key Features / Use Cases
- **Search** — query the web and get full page content back, not just links.
- **Scrape** — convert any single URL to Markdown/JSON/screenshot.
- **Crawl / Map** — pull every URL on a site, or just discover the site's URL structure.
- **Agent / Interact** — describe what data is needed in natural language, or drive a page with click/scroll/type actions before extracting.
- **MCP-ready** — connects to any AI agent or MCP client with one command, making it a common "eyes on the web" tool for agent frameworks like [[langchain-ai__langchain]].

## Related
- [[browser-use__browser-use]] — overlapping use case (giving agents access to the live web), but Firecrawl focuses on content extraction via API while browser-use drives an actual browser session.
