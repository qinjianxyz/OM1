"""Local MCP server for Rove, an OM1 useful-patrol robot demo."""

import json
import time
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rove-useful-patrol")

LOST_ITEMS: list[dict[str, str]] = []
ALERTS: list[dict[str, str]] = []


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)


@mcp.tool()
def patrol_briefing(place: str = "OM1 build night") -> str:
    """Return Rove's useful-patrol mission for the current place."""
    return _json(
        {
            "place": place,
            "mission": "Walk around, notice small useful opportunities, help safely, then return to patrol.",
            "what_counts_as_useful": [
                "confused attendee",
                "repeated resource or submission question",
                "lost object",
                "blocked path",
                "demo deadline",
                "low room energy where a short dance is welcome",
            ],
            "safety_rules": [
                "Do not identify or track people.",
                "Ask before storing personal context.",
                "Escalate uncertain safety issues to a human.",
                "Use playful motion only when it will not block or startle people.",
            ],
        }
    )


@mcp.tool()
def classify_opportunity(observation: str = "") -> str:
    """Classify a patrol observation into useful robot opportunities."""
    text = observation.lower()
    labels = []
    if any(word in text for word in ["late", "confused", "lost", "entrance"]):
        labels.append("arrival_help")
    if any(word in text for word in ["submit", "repo", "github", "config"]):
        labels.append("submission_help")
    if any(word in text for word in ["badge", "charger", "notebook", "left behind", "found"]):
        labels.append("lost_object")
    if any(word in text for word in ["mentor", "mcp", "collaborator"]):
        labels.append("matchmaking")
    if any(word in text for word in ["dance", "energy", "tired", "celebrate"]):
        labels.append("delight")
    if any(word in text for word in ["blocked", "spill", "unsafe", "emergency"]):
        labels.append("escalate")
    if not labels:
        labels.append("general_help")
    return _json(
        {
            "observation": observation,
            "opportunities": labels,
            "top_priority": labels[0],
            "recommended_next_step": "Help if safe and obvious; otherwise ask one clarifying question or escalate.",
        }
    )


@mcp.tool()
def choose_help_action(opportunity: str = "arrival_help") -> str:
    """Choose a safe speech, emotion, and movement action for an opportunity."""
    playbook = {
        "arrival_help": {
            "speech": "You look newly arrived. The build workflow is the next important step; I can point you to resources and submission.",
            "emotion": "curious",
            "move": "walk",
        },
        "submission_help": {
            "speech": "To submit, validate your OM1 config, push your fork, and paste the config link into the project form.",
            "emotion": "happy",
            "move": "stand still",
        },
        "lost_object": {
            "speech": "I found an unattended object. I can log the item and location without identifying a person.",
            "emotion": "think",
            "move": "stand still",
        },
        "matchmaking": {
            "speech": "I can make an opt-in intro for builders working on MCP and OM1 robot behavior.",
            "emotion": "excited",
            "move": "walk",
        },
        "delight": {
            "speech": "The room could use a tiny morale boost. I can do a short dance, then return to patrol.",
            "emotion": "excited",
            "move": "dance",
        },
        "escalate": {
            "speech": "This may need a human organizer. I will create a concise staff alert.",
            "emotion": "confused",
            "move": "stand still",
        },
        "general_help": {
            "speech": "I am on patrol and ready to help with resources, lost objects, or demo readiness.",
            "emotion": "curious",
            "move": "walk",
        },
    }
    return _json({"opportunity": opportunity, "action": playbook.get(opportunity, playbook["general_help"])})


@mcp.tool()
def log_lost_object(item: str = "badge", location: str = "check-in table") -> str:
    """Log an unattended object without attaching it to a person."""
    record = {
        "item": item,
        "location": location,
        "logged_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "privacy": "Object-only memory; no person identity attached.",
    }
    LOST_ITEMS.append(record)
    return _json({"logged": record, "lost_item_count": len(LOST_ITEMS)})


@mcp.tool()
def find_resource(topic: str = "OpenMind submission") -> str:
    """Return a useful event resource for the patrol robot to share."""
    resources = {
        "submission": "Project form needs project name, description, sponsor tech, team email, and GitHub repo URL.",
        "openmind": "OpenMind OM1 repo: https://github.com/OpenMind/OM1",
        "config": "Submit the OM1 config file link from the public fork.",
        "mcp": "MCP belongs inside a mode through mcp_servers with stdio, http, or sse transport.",
        "demo": "Demo should show WebSim, a mode transition, MCP call, speech/emotion/movement action, and public config link.",
    }
    lowered = topic.lower()
    for key, value in resources.items():
        if key in lowered:
            return _json({"topic": topic, "resource": value})
    return _json({"topic": topic, "resource": resources["demo"], "available_topics": sorted(resources)})


@mcp.tool()
def create_staff_alert(reason: str = "blocked path", location: str = "main room") -> str:
    """Create a concise human escalation alert."""
    alert = {
        "reason": reason,
        "location": location,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": f"Rove noticed {reason} at {location}. Human check recommended.",
    }
    ALERTS.append(alert)
    return _json({"alert": alert, "alert_count": len(ALERTS)})


@mcp.tool()
def dance_break(reason: str = "room energy is low") -> str:
    """Return a short, safe dance-break plan."""
    return _json(
        {
            "reason": reason,
            "safety_check": "Only dance if the robot has clear space and the moment is welcome.",
            "sequence": ["say why", "show excited face", "dance briefly", "return to patrol"],
            "movement": "dance",
        }
    )


@mcp.tool()
def submission_checklist(config_name: str = "rove_useful_patrol") -> str:
    """Return the project submission checklist for Rove."""
    return _json(
        {
            "project_name": "Rove: OM1 Useful Patrol",
            "config_file": f"config/{config_name}.json5",
            "repo": "https://github.com/qinjianxyz/OM1",
            "config_link": f"https://github.com/qinjianxyz/OM1/blob/main/config/{config_name}.json5",
            "description": (
                "Rove is an OM1 useful-patrol robot that walks around a space, notices small opportunities "
                "to help, uses MCP to choose a safe action, and returns to patrol."
            ),
            "technologies": "OpenMind OM1, MCP stdio server, Ollama qwen3.6, WebSim, Zenoh, Python, uv, GitHub",
        }
    )


if __name__ == "__main__":
    mcp.run()
