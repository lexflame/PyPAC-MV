
import importlib, pkgutil, inspect
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
    def instantiate_all(cls):
        for name, definition in cls.definitions.items():
            pres_cls = definition.get('presentation')
            abs_cls = definition.get('abstraction')
            ctrl_cls = definition.get('control')
            if pres_cls and abs_cls and ctrl_cls:
                pres = pres_cls()
                abs_ = abs_cls()
                agent = BaseAgent(pres, abs_, ctrl_cls)
                cls.agents[name] = agent
    @classmethod
    def get(cls, name):
        return cls.agents.get(name)

def load_agents(base_path='agents'):
    path = Path(base_path)
    for pkg in pkgutil.iter_modules([str(path)]):
        if not pkg.ispkg:
            continue
        agent_name = pkg.name
        agent_path = path / agent_name
        definition = {}
        for part in ['presentation','abstraction','control']:
            try:
                module = importlib.import_module(f'{base_path}.{agent_name}.{part}')
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BasePresentation) and part=='presentation':
                        definition['presentation'] = obj
                    elif issubclass(obj, BaseAbstraction) and part=='abstraction':
                        definition['abstraction'] = obj
                    elif issubclass(obj, BaseControl) and part=='control':
                        definition['control'] = obj
            except ModuleNotFoundError:
                continue
        meta_file = agent_path / '__meta__.py'
        meta = {'name': agent_name,'autoload':True}
        if meta_file.exists():
            spec = importlib.util.spec_from_file_location(f'{agent_name}.__meta__', str(meta_file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            meta = getattr(module,'meta',meta)
        if definition:
            AgentRegistry.register(agent_name, definition, meta)
    AgentRegistry.instantiate_all()
    return AgentRegistry.agents
