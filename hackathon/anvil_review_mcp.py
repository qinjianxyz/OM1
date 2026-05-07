"""Local MCP server for the OM1 Anvil bundle reviewer demo."""

import hashlib
import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("anvil-review")

DEFAULT_BUNDLE = Path(__file__).parent / "bundles" / "bracket-decision-om1-demo.anvilprov"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _bundle_root(bundle_path: str | None = None) -> Path:
    path = Path(bundle_path).expanduser() if bundle_path else DEFAULT_BUNDLE
    if not path.exists():
        raise FileNotFoundError(f"Bundle path does not exist: {path}")
    return path


@mcp.tool()
def summarize_bracket_case(bundle_path: str = "") -> str:
    """Summarize the customer question, recommended variant, and honest claim boundary."""
    root = _bundle_root(bundle_path or None)
    manifest = _read_json(root / "manifest.json")
    evidence = _read_json(root / "decision-evidence.json")
    solver_state = _read_json(root / "solver_state.json")

    payload = {
        "bundle_id": manifest.get("bundle_id"),
        "title": manifest.get("title"),
        "customer_question": solver_state.get("customer_question"),
        "verdict": evidence.get("verdict"),
        "claim": evidence.get("scope", {}).get("claim"),
        "claimed": evidence.get("scope", {}).get("claimed", []),
        "not_claimed": evidence.get("scope", {}).get("not_claimed", []),
        "limitation": evidence.get("limitation"),
    }
    return json.dumps(payload, indent=2)


@mcp.tool()
def verify_bundle_integrity(bundle_path: str = "") -> str:
    """Verify declared SHA-256 artifact digests in the Anvil provenance bundle."""
    root = _bundle_root(bundle_path or None)
    manifest = _read_json(root / "manifest.json")
    artifacts = manifest.get("artifacts", [])
    checked = 0
    failures: list[str] = []

    for artifact in artifacts:
        rel_path = artifact.get("path", "")
        expected = artifact.get("sha256", "")
        artifact_path = root / rel_path
        if not artifact_path.exists():
            failures.append(f"missing:{rel_path}")
            continue
        actual = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        if actual != expected:
            failures.append(f"sha256_mismatch:{rel_path}")
        else:
            checked += 1

    payload = {
        "bundle_id": manifest.get("bundle_id"),
        "schema_version": manifest.get("schema_version"),
        "artifact_count": len(artifacts),
        "checked": checked,
        "failures": failures,
        "verdict": "OK" if not failures else "FAIL",
        "note": "Integrity only: this proves declared files match the manifest, not physical certification.",
    }
    return json.dumps(payload, indent=2)


@mcp.tool()
def recommend_variant(customer_question: str = "") -> str:
    """Return the bracket variant decision with metrics and the production caveat."""
    payload = {
        "question": customer_question or "Which bracket should ship?",
        "recommendation": "V2-thickened-rib",
        "why": [
            "Loaded fundamental frequency is 39.6 Hz, above the 35 Hz servo-loop target.",
            "E-stop safety factor is 8.15 versus the minimum 1.5 gate.",
            "The cost is 46 g additional mass versus V1, but V1 and V3 fail modal clearance.",
        ],
        "reject": {
            "V1-baseline": "21.6 Hz is below the 35 Hz modal target.",
            "V3-lightened-cutout": "17.6 Hz and SF 2.41 are weaker; lowest safety margin.",
        },
        "honest_limitation": "HONEST_PARTIAL: Tet4 bending under-predicts deflection by 10-30%; upgrade to Tet10 and experimental validation before production signoff.",
        "receipt_command": "uv run src/run.py start anvil_bundle_reviewer",
    }
    return json.dumps(payload, indent=2)


if __name__ == "__main__":
    mcp.run()
