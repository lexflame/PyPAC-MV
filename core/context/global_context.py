# core/global_context.py
class GlobalContextClass:
    _registry = {}

    def set(self, name: str, value):
        self._registry[name] = value

    def get(self, name: str, default=None):
        return self._registry.get(name, default)

    def has(self, name: str) -> bool:
        return name in self._registry

    def all(self):
        return self._registry.copy()

# создаём экземпляр
GlobalContext = GlobalContextClass()

# регистрируем во встроенном пространстве имён
import builtins
builtins.GlobalContext = GlobalContext
