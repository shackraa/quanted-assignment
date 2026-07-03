# DeerFlow

**GitHub:** https://github.com/bytedance/deer-flow
**Stars:** 75,957
**Topics:** agent, agentic-framework, ai-agents, harness, multi-agent

## Overview
DeerFlow (Deep Exploration and Efficient Research Flow) is ByteDance's open-source "super agent harness" — a 2.0 ground-up rewrite that orchestrates sub-agents, long-term memory, and sandboxes to carry out long-horizon tasks, extensible via skills.

## Problem It Solves
Single-shot agent calls fall apart on tasks that take minutes to hours and require research, coding, and iteration. DeerFlow's harness coordinates sub-agents and persistent state so an agent can carry a task through many steps without losing track of the goal.

## Key Features / Use Cases
- **Sub-agents** — delegate parts of a task to specialized agents rather than one monolithic loop.
- **Sandbox mode** — isolated execution for code the agent writes.
- **Session goals & long-term memory** — the harness tracks what it's trying to accomplish and what it has already learned across a session.
- **MCP server & IM channel integration** — connects to external tools and can report progress into Slack/Discord-style channels.
- **Claude Code integration** — designed to be bootstrapped and driven by coding agents, not just human operators.

## Related
- [[ruvnet__ruflo]] and [[code-yeongyu__oh-my-openagent]] — similar "agent harness" projects that add orchestration, memory, and sub-agent coordination on top of a base coding agent.
