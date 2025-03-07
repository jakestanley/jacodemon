from enum import Enum, auto

from PySide6.QtCore import QObject, Signal
import logging

class Event(Enum):

    # MapService events
    SELECTED_MAP_UPDATED = auto()
    MAPS_UPDATED = auto()

    # MapSetService events
    SELECTED_MAPSET_UPDATED = auto()
    MAPSETS_UPDATED = auto()

    # ConfigService events
    MODS_UPDATED = auto()

    # StatsService events
    SELECTED_STATS_UPDATED = auto()

    # OptionsService events
    MODE_CHANGED = auto()

    # LaunchService events
    LAUNCH_COMPLETED = auto()

class EventService(QObject):

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._events = {}

    def register_signal(self, event_type: Event, signal: Signal):
        """Register a signal using an Enum key."""
        if event_type in self._events:
            self._logger.error(f"Event type {event_type._name_} already registered")
            return
        self._events[event_type] = signal

    def connect(self, event_type: Event, slot):
        """Allow services to subscribe to events."""
        if event_type in self._events:
            signal = self._events[event_type]
            signal.connect(slot)
