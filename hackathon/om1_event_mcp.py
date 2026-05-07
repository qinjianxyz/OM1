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
        "recommended_agent": "Forge, the OM1 Build Captain",
        "why_it_fits_om1": [
            "It is a multi-mode robot agent, not a generic app.",
            "It uses per-mode MCP tools for schedule, blueprint, checklist, and pitch help.",
            "It shows inputs, actions, background status, lifecycle hooks, transitions, and WebSim.",
            "It writes a local submission receipt so judges can inspect the result.",
        ],
        "modes": [
            "welcome: greet the judge and frame the build",
            "workshop_coach: use MCP tools to turn intent into an OM1 agent plan",
            "submission_ready: produce checklist, pitch, and receipt",
        ],
        "actions": ["speak", "emotion", "submission_receipt"],
        "inputs": ["GoogleASRInput", "MockInput", "OM1EventCueInput", "ConversationHistoryInput"],
        "backgrounds": ["OM1EventStatusBackground"],
        "mcp_tools": [
            "get_event_schedule",
            "recommend_agent_blueprint",
            "submission_checklist",
            "generate_demo_pitch",
        ],
    }
    return json.dumps(payload, indent=2)


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
                f"uv run src/run.py start {config_name}",
            ],
            "judge_prompt": "Ask: What should I build tonight, and how do I submit it cleanly?",
        },
        indent=2,
    )


@mcp.tool()
def generate_demo_pitch(agent_name: str = "Forge") -> str:
    """Generate a short live-demo pitch for the builder event."""
    return json.dumps(
        {
            "opening": f"{agent_name} is an OM1 robot build captain for this event.",
            "demo_flow": [
                "The judge asks what to build.",
                "The agent switches into workshop coach mode.",
                "It calls MCP tools for schedule, blueprint, checklist, and pitch.",
                "It speaks the plan, changes expression, and writes a receipt.",
                "The submission link points to the config file in the fork.",
            ],
            "closer": "This is OM1 as an embodied builder workflow, using the exact workshop primitives.",
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()

