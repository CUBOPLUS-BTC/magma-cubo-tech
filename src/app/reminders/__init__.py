"""Reminders module for remittances.

Schedules monthly / biweekly / custom reminders that fire a notification
through webhook, Nostr DM, or email. Integrates with the existing
``scheduler/scheduler.py`` so it does not spawn its own background thread.
"""

from .manager import RemindersManager
from .dispatcher import ReminderDispatcher

__all__ = ["RemindersManager", "ReminderDispatcher"]
