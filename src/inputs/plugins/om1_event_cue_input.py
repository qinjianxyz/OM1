import asyncio
import time
from pathlib import Path
from typing import Optional

from pydantic import Field

from inputs.base import Message, SensorConfig
from inputs.base.loop import FuserInput
from providers.io_provider import IOProvider


class OM1EventCueConfig(SensorConfig):
    """Configuration for scripted OM1 event cues."""

    cue_file: str = Field(default="hackathon/om1_event_cues.txt")
    input_name: str = Field(default="Builder Prompt")
    interval_seconds: float = Field(default=2.0)
    repeat: bool = Field(default=False)


class OM1EventCueInput(FuserInput[OM1EventCueConfig, Optional[str]]):
    """Emit a scripted builder-event prompt for no-microphone demos."""

    def __init__(self, config: OM1EventCueConfig):
        super().__init__(config)
        self.io_provider = IOProvider()
        self.descriptor_for_LLM = config.input_name
        self.messages: list[Message] = []
        self._last_emit = 0.0
        self._index = 0
        self._cues = self._load_cues()

    def _load_cues(self) -> list[str]:
        path = Path(self.config.cue_file)
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.exists():
            return []
        return [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    async def _poll(self) -> Optional[str]:
        await asyncio.sleep(0.2)
        if not self._cues:
            return None
        now = time.time()
        if now - self._last_emit < self.config.interval_seconds:
            return None
        if self._index >= len(self._cues):
            if not self.config.repeat:
                return None
            self._index = 0
        self._last_emit = now
        cue = self._cues[self._index]
        self._index += 1
        return cue

    async def _raw_to_text(self, raw_input: Optional[str]) -> Optional[Message]:
        if raw_input is None:
            return None
        return Message(timestamp=time.time(), message=raw_input)

    async def raw_to_text(self, raw_input: Optional[str]):
        message = await self._raw_to_text(raw_input)
        if message is not None:
            self.messages.append(message)

    def formatted_latest_buffer(self) -> Optional[str]:
        if not self.messages:
            return None
        message = self.messages[-1]
        self.io_provider.add_input(self.descriptor_for_LLM, message.message, message.timestamp)
        self.messages = []
        return f"""
INPUT: {self.descriptor_for_LLM}
// START
{message.message}
// END
"""

