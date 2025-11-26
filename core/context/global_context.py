
import builtins
import importlib
import inspect
import json
import os
import traceback

class GLC:
    _registry = {}

    def test(obj,data = False):
        print(data)

    def set(self, name: str, value):
        self._registry[name] = value

    def get(self, name: str, default=None):
        return self._registry.get(name, default)

    def has(self, name: str) -> bool:
        return name in self._registry

    def all(self):
        return self._registry.copy()

    def expose_log(data,obj = False):
        """Гибкий вывод для отладки (аналог jq/print_r)"""
        qt_type = type(obj).__name__
        qt_module = type(obj).__module__
        if qt_module.startswith("PyQt"):
            if hasattr(obj, "text"):
                print(f"<{qt_type} text='{obj.text()}' data={obj.data(256) if hasattr(obj, 'data') else None}>")
            elif hasattr(obj, "objectName"):
                print(f"<{qt_type} objectName='{obj.objectName()}'>")
            else:
                print(f"<{qt_type}>")
            return

        if isinstance(obj, (dict, list, tuple, set)):
            try:
                print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))
                return
            except Exception:
                pass

        if hasattr(obj, "__dict__"):
            attrs = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
            print(f"[bold cyan]{obj.__class__.__name__}[/bold cyan]:")
            print(json.dumps(attrs, indent=2, ensure_ascii=False, default=str))
            return

        print(obj)



    def init_class(classes, caller = False):

        trace = traceback.extract_stack()
        stack_func = inspect.stack()
        path_init = {}

        caller_frame = trace[-2]
        stack_frame = stack_func[1]

        script_name = os.path.basename(caller_frame.filename).split('.')[0]
        module_data = inspect.getmodule(inspect.stack()[1].frame)
        module_path_import = module_data.__name__ if module_data else "unknown"
        item = 'item'
        path_init['parent'] = {}
        path_init['parent']['module_data'] = module_data
        path_init['parent']['module_path_import'] = module_path_import
        path_init['parent']['classes'] = (f"{module_path_import}.{script_name}_classes")
        path_init['parent']['file'] = (f"{stack_func[1].filename.replace((f"{script_name}.py"), "")}{script_name}_classes")
        if item in path_init['parent']['classes']:
            path_init['parent']['is_item'] = True
            path_init['parent']['file'] = (f"{stack_func[1].filename.replace((f"{script_name}.py"), "")}behavior")

        files = scan_folder(path_init['parent']['file'], recursive=True)
        result = {}
        for file_item in files:
            module = file_item['module']
            class_name = file_item['name_class']
            path = file_item['import_path']
            try:
                cls = getattr(module, class_name)
                result[class_name] = cls()
            except Exception as e:
                print(f"Ошибка импорта {class_name} из {path}: {e}")
                result[class_name]['instance'] = None
                result[class_name]['class'] = None
        return result

# создаём экземпляр
GLC = GLC()
# регистрируем во встроенном пространстве имён
builtins.GLC = GLC
builtins.expose_log = GLC.expose_log
