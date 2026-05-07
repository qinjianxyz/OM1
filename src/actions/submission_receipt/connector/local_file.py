import logging
import time
from pathlib import Path

from pydantic import Field

from actions.base import ActionConfig, ActionConnector
from actions.submission_receipt.interface import SubmissionReceiptInput


class SubmissionReceiptLocalFileConfig(ActionConfig):
    """Configuration for the local event receipt writer."""

    output_dir: str = Field(default="hackathon/receipts")
    filename: str = Field(default="rove_submission_receipt.md")


class SubmissionReceiptLocalFileConnector(ActionConnector[SubmissionReceiptLocalFileConfig, SubmissionReceiptInput]):
    """Write a submission receipt to a local markdown file."""

    async def connect(self, output_interface: SubmissionReceiptInput) -> None:
        output_dir = Path(self.config.output_dir)
        if not output_dir.is_absolute():
            output_dir = Path.cwd() / output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / self.config.filename

        body = "\n".join(
            [
                "# OM1 Builder Event Submission Receipt",
                "",
                f"- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"- Agent: {output_interface.agent_name or 'Rove'}",
                f"- Concept: {output_interface.concept or 'OM1 useful patrol robot'}",
                f"- Modes: {output_interface.modes or 'patrol, assist, object_steward, delight, submission_ready'}",
                f"- MCP tools: {output_interface.mcp_tools or 'patrol briefing, opportunity classifier, help action, object log, resource lookup, staff alert, dance break, submission checklist'}",
                f"- Checklist: {output_interface.checklist or 'Validate config, run modes, open WebSim, push public config link'}",
                f"- Demo script: {output_interface.demo_script or 'Ask Rove to patrol, help a builder, remember an unattended object, and do a safe dance break'}",
                "",
            ]
        )
        output_path.write_text(body, encoding="utf-8")
        logging.info(f"Submission receipt written to {output_path}")
