"""Drive the Rove WebSim demo through OM1 MockInput ports.

Run after starting:
    uv run src/run.py rove_useful_patrol --log-level INFO
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time
from typing import Any, Iterable

import websockets

MOCK_PORTS = (8787, 8788, 8789, 8790, 8791)
WEBSIM_URL = "ws://localhost:8000/ws"


async def read_websim_state() -> dict[str, Any]:
    async with websockets.connect(WEBSIM_URL) as ws:
        message = await asyncio.wait_for(ws.recv(), timeout=5)
        return json.loads(message)


async def send_to_active_mock_input(text: str, ports: Iterable[int] = MOCK_PORTS) -> int:
    last_error = ""
    for port in ports:
        try:
            async with websockets.connect(f"ws://localhost:{port}") as ws:
                await ws.send(text)
                await asyncio.wait_for(ws.recv(), timeout=3)
                return port
        except Exception as exc:  # noqa: BLE001 - demo driver reports all failed ports.
            last_error = f"{type(exc).__name__}: {exc}"
    raise RuntimeError(f"No active MockInput port accepted the prompt. Last error: {last_error}")


async def wait_for_action(expected_action: str, timeout_seconds: int = 95) -> tuple[dict[str, Any], bool]:
    deadline = time.time() + timeout_seconds
    latest: dict[str, Any] = {}
    while time.time() < deadline:
        latest = await read_websim_state()
        if latest.get("current_action") == expected_action:
            return latest, True
        await asyncio.sleep(3)
    return latest, False


def print_state(label: str, state: dict[str, Any]) -> None:
    print(f"\n== {label} ==")
    print(f"action:  {state.get('current_action')}")
    print(f"emotion: {state.get('current_emotion')}")
    print(f"speech:  {state.get('last_speech')}")


async def run_dance() -> None:
    prompt = "The room energy is dropping and someone asks if the robot can dance. Space is clear."
    port = await send_to_active_mock_input(prompt)
    print(f"sent dance cue on port {port}")
    state, ok = await wait_for_action("dance")
    print_state("dance receipt", state)
    if not ok:
        raise SystemExit("dance action was not observed before timeout")


async def run_submission() -> None:
    prompt = "Ready to submit. What should go in the project form and receipt?"
    port = await send_to_active_mock_input(prompt)
    print(f"sent submission cue on port {port}")
    state, ok = await wait_for_action("stand still")
    print_state("submission receipt", state)
    if not ok:
        raise SystemExit("submission stand-still action was not observed before timeout")


async def run_snapshot() -> None:
    print_state("current WebSim state", await read_websim_state())


async def run_story() -> None:
    print("waiting for baseline patrol receipt...")
    state, ok = await wait_for_action("walk", timeout_seconds=120)
    print_state("baseline patrol receipt", state)
    if not ok:
        raise SystemExit("baseline patrol action was not observed before timeout")

    print("\ntriggering safe dance cue...")
    await run_dance()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Drive Rove's OM1 WebSim demo.")
    parser.add_argument(
        "scenario",
        choices=("snapshot", "dance", "submission", "story"),
        help="Demo cue to send.",
    )
    args = parser.parse_args()

    if args.scenario == "snapshot":
        await run_snapshot()
    elif args.scenario == "dance":
        await run_dance()
    elif args.scenario == "submission":
        await run_submission()
    elif args.scenario == "story":
        await run_story()


if __name__ == "__main__":
    asyncio.run(main())
