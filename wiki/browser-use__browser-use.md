# browser-use

**GitHub:** https://github.com/browser-use/browser-use
**Stars:** 102,283
**Topics:** ai-agents, browser-automation, llm, playwright

## Overview
browser-use gives an AI agent a real, controllable browser instead of an API abstraction over it. It's built on the premise that the latest models do better with a direct, dependable browser surface than with heavily pre-abstracted tooling.

## Problem It Solves
A lot of the internet — logins, dynamic UIs, multi-step flows like checkout or job applications — isn't reachable through clean scraping APIs; it requires actually clicking, typing, and navigating like a human would. browser-use lets an agent do that directly, headless or visibly.

## Key Features / Use Cases
- **Agent-driven browsing** — point an agent at a task ("apply to this job with my resume") and it drives the browser end-to-end.
- **CLI 3.0** — lets coding agents (Claude Code, Codex) control a browser via a Python-scriptable CLI, backed by "Browser Harness."
- **Cloud option** — hosted browsers with proxy rotation, captcha solving, and 1000+ service integrations for production use.
- **Custom tools** — extend the agent with domain-specific tools when the default action set isn't enough.

## Related
- [[firecrawl__firecrawl]] — complementary web-access tooling; browser-use is for interactive, stateful browser tasks, Firecrawl is for bulk content extraction.
