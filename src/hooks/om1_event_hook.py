"""Credit-free lifecycle hooks for the OM1 builder-event submission."""

import logging
import time
from typing import Any

from providers.io_provider import IOProvider


def record_local_event_hook(context: dict[str, Any]) -> bool:
    """Record lifecycle state locally without invoking cloud TTS."""
    phase = context.get("phase") or context.get("mode_name") or "OM1 event"
    message = f"{phase}: local lifecycle hook executed without cloud speech."
    IOProvider().add_input("Lifecycle Hook", message, time.time())
    logging.info(message)
    return True
