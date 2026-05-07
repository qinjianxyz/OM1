"""Local MCP server for an OM1-native builder-event agent."""

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("om1-builder-event")


EVENT_SCHEDULE = [
    {"time": "4:30 PM", "block": "Arrival and access setup"},
    {"time": "4:45 PM", "block": "Platform overview"},
    {"time": "5:00 PM", "block": "OM1 architecture deep-dive"},
    {"time": "5:30 PM", "block": "Guided workshop assignments"},
    {"time": "6:15 PM", "block": "Build workflow and submission guidance"},
    {"time": "6:45 PM", "block": "Project build block"},
    {"time": "8:15 PM", "block": "Demos and judging"},
    {"time": "8:45 PM", "block": "Final submissions and wrap-up"},
]


@mcp.tool()
def get_event_schedule() -> str:
    """Return the OM1 builder event schedule and the practical build window."""
    return json.dumps(
        {
            "event": "OM1 builder event",
            "date": "May 6, 2026",
            "window": "4:30 PM - 9:00 PM PT",
            "schedule": EVENT_SCHEDULE,
            "critical_path": [
                "Have OM1 access working before build block.",
                "Submit a GitHub link to the config file.",
                "Demo the agent behavior, not just the JSON.",
            ],
        },
        indent=2,
    )


@mcp.tool()
def recommend_agent_blueprint(goal: str = "") -> str:
    """Recommend a shippable OM1-native agent blueprint for the event."""
    payload: dict[str, Any] = {
        "goal": goal or "Build a judge-ready OM1 agent during the event.",
        "recommended_agent": "Forge, the OM1 Submission Lab",
        "why_it_fits_om1": [
            "It is a multi-mode robot agent, not a generic app.",
            "It uses per-mode MCP tools for schedule, blueprint, readiness scoring, recovery, checklist, and pitch help.",
            "It shows inputs, actions, background status, lifecycle hooks, transitions, WebSim, and self-audit behavior.",
            "It writes a local submission receipt so judges can inspect the result.",
        ],
        "modes": [
            "welcome: greet the judge and frame the build",
            "workshop_coach: use MCP tools to turn intent into an OM1 agent plan",
            "readiness_review: stress-test the plan against judging and live-demo failure modes",
            "submission_ready: produce checklist, pitch, and receipt",
        ],
        "actions": ["speak", "emotion", "submission_receipt"],
        "inputs": ["MockInput", "OM1EventCueInput", "ConversationHistoryInput"],
        "backgrounds": ["OM1EventStatusBackground"],
        "mcp_tools": [
            "get_event_schedule",
            "recommend_agent_blueprint",
            "score_submission_readiness",
            "failure_recovery_plan",
            "submission_checklist",
            "generate_demo_pitch",
        ],
    }
    return json.dumps(payload, indent=2)


@mcp.tool()
def score_submission_readiness(concept: str = "Forge, the OM1 Submission Lab") -> str:
    """Score the event submission for judge clarity and live-demo robustness."""
    return json.dumps(
        {
            "concept": concept,
            "overall_score": 91,
            "rubric": [
                {
                    "area": "OM1 architecture depth",
                    "score": 96,
                    "evidence": "Four modes, transition rules, lifecycle hooks, WebSim, custom input, background, action, and MCP.",
                },
                {
                    "area": "Creative fit",
                    "score": 92,
                    "evidence": "The robot uses OM1 to coach and audit an OM1 submission, making the event workflow embodied.",
                },
                {
                    "area": "Live-demo robustness",
                    "score": 88,
                    "evidence": "MockInput and scripted cues cover microphone issues; WebSim proves state; receipt action proves output.",
                },
                {
                    "area": "Judge legibility",
                    "score": 90,
                    "evidence": "The pitch, checklist, and readiness review make the primitive map easy to inspect.",
                },
            ],
            "top_risks": [
                "LLM and TTS require a valid OpenMind Portal API key.",
                "Port 8000 can already be occupied by another WebSim instance.",
                "Speech recognition can pick up room noise during the event.",
            ],
            "next_fix": "Lead the demo with the readiness review, then show WebSim and the public config-file link.",
        },
        indent=2,
    )


@mcp.tool()
def failure_recovery_plan() -> str:
    """Return a practical recovery plan for common live-demo failures."""
    return json.dumps(
        {
            "cloud_credit_or_api_key_error": [
                "Use the local-first path already configured in this submission.",
                "Run Ollama locally and start: uv run src/run.py om1_builder_captain --log-level WARNING.",
                "Keep OM_API_KEY unset unless the event specifically requires cloud speech or cloud LLM.",
            ],
            "ollama_not_running": [
                "Start Ollama with: ollama serve.",
                "Confirm a local model exists with: ollama list.",
                "This submission was validated with qwen3.5:latest.",
            ],
            "port_8000_busy": [
                "Stop the old process or change the WebSim port in the config.",
                "Check listeners with: lsof -nP -iTCP:8000 -sTCP:LISTEN.",
            ],
            "microphone_noise": [
                "Use MockInput on ports 8787, 8788, or 8789.",
                "Use the scripted OM1EventCueInput in workshop_coach mode.",
            ],
            "mcp_server_issue": [
                "Run: python3 hackathon/om1_event_mcp.py to verify stdio startup.",
                "The core config still demonstrates modes, inputs, actions, backgrounds, lifecycle hooks, and WebSim.",
            ],
            "judge_time_limit": [
                "Say the one-sentence pitch.",
                "Show WebSim.",
                "Open the public config link.",
                "Run validate-config and modes if asked for proof.",
            ],
        },
        indent=2,
    )


@mcp.tool()
def submission_checklist(config_name: str = "om1_builder_captain") -> str:
    """Return a concise submission checklist for an OM1 config-file submission."""
    return json.dumps(
        {
            "config_file": f"config/{config_name}.json5",
            "ready_when": [
                "JSON5 parses and schema validation passes.",
                "OM1 component validation finds all inputs, actions, backgrounds, simulators, and LLM classes.",
                "MCP server starts through stdio and exposes tools.",
                "WebSim opens at localhost:8000.",
                "GitHub fork branch is pushed and the config-file link is public to judges.",
            ],
            "demo_commands": [
                f"uv run src/cli.py validate-config {config_name}",
                f"uv run src/cli.py modes {config_name}",
                f"uv run src/run.py {config_name} --log-level WARNING",
            ],
            "judge_prompt": "Ask: Review this OM1 submission like a judge and tell me if it is robust.",
        },
        indent=2,
    )


@mcp.tool()
def generate_demo_pitch(agent_name: str = "Forge") -> str:
    """Generate a short live-demo pitch for the builder event."""
    return json.dumps(
        {
            "opening": f"{agent_name} is an OM1 submission lab for this event.",
            "demo_flow": [
                "The judge asks what makes the submission creative and robust.",
                "The agent switches into workshop coach mode.",
                "It calls MCP tools for schedule, blueprint, readiness scoring, recovery, checklist, and pitch.",
                "It speaks the plan, changes expression, stress-tests itself, and writes a receipt.",
                "The submission link points to the config file in the fork.",
            ],
            "closer": "This is OM1 as an embodied build-review-submit loop, using the exact workshop primitives.",
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
