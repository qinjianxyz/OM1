import logging
import time
from pathlib import Path

from pydantic import Field

from actions.base import ActionConfig, ActionConnector
from actions.review_receipt.interface import ReviewReceiptInput


class ReviewReceiptLocalFileConfig(ActionConfig):
    """Configuration for the local receipt writer."""

    output_dir: str = Field(default="hackathon/receipts")
    filename: str = Field(default="latest_review_receipt.md")


class ReviewReceiptLocalFileConnector(ActionConnector[ReviewReceiptLocalFileConfig, ReviewReceiptInput]):
    """Write review receipts to a local markdown file for demo handoff."""

    async def connect(self, output_interface: ReviewReceiptInput) -> None:
        output_dir = Path(self.config.output_dir)
        if not output_dir.is_absolute():
            output_dir = Path.cwd() / output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / self.config.filename

        body = "\n".join(
            [
                "# OM1 Anvil Review Receipt",
                "",
                f"- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"- Verdict: {output_interface.verdict or 'UNSPECIFIED'}",
                f"- Decision: {output_interface.decision or 'UNSPECIFIED'}",
                f"- Evidence: {output_interface.evidence or 'UNSPECIFIED'}",
                f"- Limitation: {output_interface.limitation or 'UNSPECIFIED'}",
                f"- Reproduce: `{output_interface.command or 'UNSPECIFIED'}`",
                "",
            ]
        )
        output_path.write_text(body, encoding="utf-8")
        logging.info(f"Review receipt written to {output_path}")

