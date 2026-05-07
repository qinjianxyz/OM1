import time

from pydantic import Field

from backgrounds.base import Background, BackgroundConfig
from providers.io_provider import IOProvider


class AnvilReviewerStatusConfig(BackgroundConfig):
    """Configuration for the local reviewer-status heartbeat."""

    status_name: str = Field(default="Reviewer Status")
    bundle_id: str = Field(default="bracket-decision-om1-demo")
    interval_seconds: float = Field(default=3.0)


class AnvilReviewerStatusBackground(Background[AnvilReviewerStatusConfig]):
    """Publish a visible local status heartbeat for WebSim without robot hardware."""

    def __init__(self, config: AnvilReviewerStatusConfig):
        super().__init__(config)
        self.io_provider = IOProvider()

    def run(self) -> None:
        value = (
            f"Monitoring {self.config.bundle_id}: integrity check ready, "
            "decision gate is V2 >= 35 Hz and SF >= 1.5, limitations must be spoken."
        )
        self.io_provider.add_input(self.config.status_name, value, time.time())
        self.sleep(self.config.interval_seconds)
