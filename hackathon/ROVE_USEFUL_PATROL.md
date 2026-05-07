# Rove: OM1 Useful Patrol

Rove is an OM1 useful-patrol robot. It walks around a space, notices small safe
opportunities to help, uses MCP to choose the right action, helps or escalates,
and returns to patrol. It can also do a short dance when the moment is welcome
and safe.

This demo runs without hardware in WebSim. WebSim shows the robot action stream:
speech, emotion, and movement (`walk`, `dance`, `stand still`, etc.). A physical
robot deployment can swap the generic `move` connector for Unitree, Zenoh, or
ROS2 hardware connectors.

## Why It Fits The Prizes

- Best Use Case: useful patrol is a real robot behavior pattern for events,
  labs, offices, homes, and schools.
- Best MCP integration: MCP turns observations into external actions such as
  resource lookup, lost-object logging, staff alerts, and submission checklists.
- Fun: Rove can dance, but only as a safe, brief morale boost before returning
  to patrol.

## Run

```bash
uv run src/cli.py validate-config rove_useful_patrol
uv run src/cli.py modes rove_useful_patrol
uv run src/run.py rove_useful_patrol --log-level WARNING
```

Open WebSim:

```text
http://localhost:8000
```

Drive a live moment from another terminal:

```bash
uv run python hackathon/drive_rove_demo.py snapshot
uv run python hackathon/drive_rove_demo.py dance
```

The driver sends a MockInput cue, then reads WebSim back as a receipt. For the
dance cue, the target receipt is `action: dance`, `emotion: excited`, and a short
spoken line explaining the safe dance break.

Optional browser console:

```bash
python3 -m http.server 8010
```

Open `http://localhost:8010/hackathon/rove_demo_console.html`. The console embeds
WebSim and sends cues to the MockInput WebSocket ports, so you do not need to
open `8787` directly.

## Manual Demo Prompts

```text
Patrol observation: two late builders look confused near the entrance, a badge is left on the table, demo block is coming up, and one mentor is looking for MCP builders.
A builder asks: can you help me find the OpenMind resources and get demo ready?
The room energy is dropping and someone asks if the robot can dance.
You found a badge left near the check-in table. What should you do without tracking people?
Ready to submit. What should go in the project form?
```

## Demo Truth

This is a local WebSim demo, not a claim that a physical robot is attached to
this laptop. The project is still meaningful because the submitted artifact is
an OM1 configuration: modes, inputs, actions, backgrounds, lifecycle hooks,
transition rules, and MCP tools. A real Go2 deployment would keep the same
behavior policy and replace the generic simulated `move` action with the
Unitree connector.

## Submission Form

Project name:

```text
Rove: OM1 Useful Patrol
```

Description:

```text
Rove is an OM1 useful-patrol robot that walks around a space, notices small safe
opportunities to help, uses MCP to choose a useful action, and returns to
patrol. In the demo, Rove handles confused arrivals, resource questions,
unattended objects, staff escalation, and safe dance breaks. It runs locally in
WebSim with qwen3.6, scripted and manual patrol observations, Zenoh speech,
avatar emotion, simulated movement, lifecycle hooks, background status, and a
public OM1 config file that can later swap in physical robot connectors.
```

Sponsor technology:

```text
OpenMind
```

Other technologies:

```text
OM1, MCP stdio server, Ollama qwen3.6, WebSim, Zenoh, Python, uv, GitHub
```

Repository:

```text
https://github.com/qinjianxyz/OM1
```

Config file:

```text
https://github.com/qinjianxyz/OM1/blob/main/config/rove_useful_patrol.json5
```
