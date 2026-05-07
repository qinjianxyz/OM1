# OM1 Anvil Bundle Reviewer

Hackathon submission surface:

- `config/anvil_bundle_reviewer.json5` is the config-file link to submit.
- `hackathon/anvil_review_mcp.py` is a local stdio MCP server with three tools:
  `summarize_bracket_case`, `verify_bundle_integrity`, and `recommend_variant`.
- `hackathon/bundles/bracket-decision-om1-demo.anvilprov` is a tiny checked-in
  demo bundle with SHA-256 artifact verification.
- `src/inputs/plugins/anvil_bundle_cue_input.py` gives a no-microphone scripted cue.
- `src/backgrounds/plugins/anvil_reviewer_status.py` gives WebSim a continuous status heartbeat.
- `src/actions/review_receipt/connector/local_file.py` writes a local markdown review receipt.

Demo line:

> "Can I trust this robot-arm bracket simulation, and which variant should ship?"

Run:

```bash
export OM_API_KEY="<your OpenMind key>"
uv run src/cli.py validate-config anvil_bundle_reviewer --no-check-components
uv run src/run.py start anvil_bundle_reviewer
```

Open WebSim at http://localhost:8000.

The honest decision:

- Ship `V2-thickened-rib`.
- It clears the 35 Hz modal gate with 39.6 Hz and has SF 8.15 under e-stop.
- Carry the limitation: this is `HONEST_PARTIAL`, not certification evidence; Tet4 bending under-predicts deflection by 10-30%.
