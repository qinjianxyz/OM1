# OM1 Submission Lab

This is a pure OM1 event submission. It does not depend on any outside product
story or paid cloud credits. The point is to demonstrate that OM1 is open enough
to run a self-hosted robot-agent workflow: local model, local MCP, WebSim,
scripted inputs, local actions, and a public config-file submission.

Submit this config link:

```text
config/om1_builder_captain.json5
```

What it demonstrates:

- Multi-mode OM1 config: `welcome`, `workshop_coach`, `readiness_review`, `submission_ready`
- Per-mode MCP server: `hackathon/om1_event_mcp.py`
- Local-first LLM: `OllamaLLM` with `qwen3.5:latest`
- Inputs: `MockInput`, `OM1EventCueInput`, `ConversationHistoryInput`
- Actions: `speak` over Zenoh, `face`, `submission_receipt`
- Background: `OM1EventStatusBackground`
- Lifecycle hooks, transition rules, WebSim, readiness scoring, and failure recovery

Creative angle:

Forge is an embodied submission lab. It uses OM1 to design, audit, recover, and
submit an OM1 agent. If cloud credits are gone, the same config still runs
locally because the brain is Ollama and the tools are local MCP.

Run:

```bash
uv run src/cli.py validate-config om1_builder_captain
uv run src/cli.py modes om1_builder_captain
uv run src/run.py om1_builder_captain --log-level WARNING
```

Open WebSim at http://localhost:8000.

The fork is public at https://github.com/qinjianxyz/OM1, so judges can open the
config-file link directly from the pushed branch.

No-credit prerequisites:

```bash
ollama serve
ollama pull qwen3.5
```

Demo prompt:

> Review this OM1 submission like a judge and tell me if it is creative and robust.

Fast fallback if the local model is not ready: run `validate-config`, run `modes`,
open WebSim, and show the MCP smoke output from `hackathon/om1_event_mcp.py`.
