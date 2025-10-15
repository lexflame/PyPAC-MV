import importlib, pkgutil, inspect, importlib.util, json
from pathlib import Path
from core.base import BaseAgent, BasePresentation, BaseAbstraction, BaseControl

class AgentRegistry:
    agents = {}
    definitions = {}
    metadata = {}
    @classmethod
    def register(cls, name, definition, meta=None):
        cls.definitions[name] = definition
        if meta:
            cls.metadata[name] = meta
    @classmethod
    def instantiate_all(cls, autoload_only=True):
        for name, definition in cls.definitions.items():
            meta = cls.metadata.get(name, {})
            if autoload_only and not meta.get("autoload", True):
                continue
            pres_cls = definition.get('presentation')
            abs_cls = definition.get('abstraction')
            ctrl_cls = definition.get('control')
            if pres_cls and abs_cls and ctrl_cls:
                pres = pres_cls()
                abs_ = abs_cls()
                agent = BaseAgent(pres, abs_, ctrl_cls)
                cls.agents[name] = agent
                print(f"[PyPAC-MV OK] ✅ Агент загружен: {name}")
            else:
                print(f"[PyPAC-MV WARNING] load_agents - ⚠️ Агент {name} — неполный набор классов")
    @classmethod
    def get(cls, name):
        return cls.agents.get(name)

def _load_meta(agent_path: Path) -> dict:
    meta_file = agent_path / '__meta__.py'
    json_file = agent_path / 'manifest.json'
    if json_file.exists():
        try:
            return json.load(open(json_file, 'r', encoding='utf-8'))
        except Exception:
            return {"name": agent_path.name, "autoload": True}
    if meta_file.exists():
        spec = importlib.util.spec_from_file_location(f"{agent_path.name}.__meta__", str(meta_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "meta", {})
    return {"name": agent_path.name, "autoload": True}

def load_agents(base_path='agents'):
    path = Path(base_path)
    if not path.exists():
        print(f"[PyPAC-MV ERROR] load_agents - ❌ Нет каталога {base_path}")
        return {}
    for pkg in pkgutil.iter_modules([str(path)]):
        if not pkg.ispkg:
            continue
        agent_name = pkg.name
        agent_path = path / agent_name
        print(f"[PyPAC-MV] 🔍 Найден агент: {agent_name}")
        definition = {}
        meta = _load_meta(agent_path)
        for part in ['presentation','abstraction','control']:
            try:
                module = importlib.import_module(f'{base_path}.{agent_name}.{part}')
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    try:
                        if issubclass(obj, BasePresentation) and part=='presentation':
                            definition['presentation'] = obj
                        elif issubclass(obj, BaseAbstraction) and part=='abstraction':
                            definition['abstraction'] = obj
                        elif issubclass(obj, BaseControl) and part=='control':
                            definition['control'] = obj
                    except TypeError:
                        if part=='presentation' and obj.__name__.lower().endswith('presentation'):
                            definition['presentation'] = obj
                        if part=='abstraction' and obj.__name__.lower().endswith('abstraction'):
                            definition['abstraction'] = obj
                        if part=='control' and obj.__name__.lower().endswith('control'):
                            definition['control'] = obj
            except ModuleNotFoundError:
                continue
        if definition:
            AgentRegistry.register(agent_name, definition, meta)
        else:
            print(f"[PyPAC-MV WARNING] load_agents ⚠️ Агент {agent_name} не зарегистрирован (нет классов)")
    AgentRegistry.instantiate_all()
    return AgentRegistry.agents
