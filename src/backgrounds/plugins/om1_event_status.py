import time

from pydantic import Field

from backgrounds.base import Background, BackgroundConfig
from providers.io_provider import IOProvider


class OM1EventStatusConfig(BackgroundConfig):
    """Configuration for the OM1 builder-event status heartbeat."""

    status_name: str = Field(default="Event Status")
    phase: str = Field(default="Build block")
    mission: str = Field(
        default="build a multi-mode OM1 config, verify it, push to a fork, and submit the config-file link.",
    )
    interval_seconds: float = Field(default=3.0)


class OM1EventStatusBackground(Background[OM1EventStatusConfig]):
    """Publish a visible workshop status heartbeat for WebSim."""

    def __init__(self, config: OM1EventStatusConfig):
        super().__init__(config)
        self.io_provider = IOProvider()

    def run(self) -> None:
        value = f"{self.config.phase}: {self.config.mission}"
        self.io_provider.add_input(self.config.status_name, value, time.time())
        self.sleep(self.config.interval_seconds)
