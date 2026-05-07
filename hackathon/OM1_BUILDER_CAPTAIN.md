# OM1 Builder Captain

This is a pure OM1 event submission. It does not depend on any outside product
story. The point is to demonstrate the workshop primitives directly.

Submit this config link:

```text
config/om1_builder_captain.json5
```

What it demonstrates:

- Multi-mode OM1 config: `welcome`, `workshop_coach`, `submission_ready`
- Per-mode MCP server: `hackathon/om1_event_mcp.py`
- Inputs: `GoogleASRInput`, `MockInput`, `OM1EventCueInput`, `ConversationHistoryInput`
- Actions: `speak`, `face`, `submission_receipt`
- Background: `OM1EventStatusBackground`
- Lifecycle hooks, transition rules, and WebSim

Run:

```bash
export OM_API_KEY="<your OpenMind key>"
uv run src/cli.py validate-config om1_builder_captain
uv run src/cli.py modes om1_builder_captain
uv run src/run.py om1_builder_captain
```

Open WebSim at http://localhost:8000.

The fork is public at https://github.com/qinjianxyz/OM1, so judges can open the
config-file link directly from the pushed branch.

If WebSim opens but LLM or speech calls show `401 malformed API key`, export the
OpenMind Portal key for the event:

```bash
export OM_API_KEY="<your OpenMind key>"
```

Demo prompt:

> What should I build tonight, and how do I submit it cleanly?
