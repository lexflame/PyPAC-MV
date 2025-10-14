from typing import Callable

class EventBus:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._listeners = {}
        return cls._instance
    def on(self, event: str, callback: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    def emit(self, event: str, *args, **kwargs):
        if event in self._listeners:
            for cb in list(self._listeners[event]):
                try:
                    cb(*args, **kwargs)
                except Exception as e:
                    print(f"[EventBus] handler error: {e}")
