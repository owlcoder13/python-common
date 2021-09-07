from common.data import getattrdot
import importlib
import importlib.util


def import_dyn(mod_path):
    """
    Dynamic import module
    """
    full_part = list()

    for part in mod_path.split('.'):
        try:
            tmp = full_part.copy()
            tmp.append(part)
            importlib.util.find_spec('.'.join(tmp))
            full_part = tmp
        except ModuleNotFoundError:
            return importlib.import_module('.'.join(full_part))


def import_get_path(mod_path):
    """
    Dynamic import module + get rest of path
    """
    mod = import_dyn(mod_path)
    last = mod_path[len(mod.__name__) + 1:]
    return getattrdot(mod, last)
