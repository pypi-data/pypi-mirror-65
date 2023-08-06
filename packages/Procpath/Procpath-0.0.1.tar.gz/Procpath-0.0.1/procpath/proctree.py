import logging
import os


__all__ = 'Tree', 'flatten'

logger = logging.getLogger(__package__)


def get_pid_list():
    return [int(p) for p in os.listdir('/proc') if p.isdigit()]


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class Tree:

    _proc_file_registry = None

    _skip_self = None
    _dictcls = None

    def __init__(self, proc_file_registry, skip_self=True, dictcls=AttrDict):
        self._proc_file_registry = proc_file_registry
        self._skip_self = skip_self
        self._dictcls = dictcls

    def _read_process_dict(self, pid):
        result = self._dictcls()
        for name, fn in self._proc_file_registry.items():
            try:
                with open(f'/proc/{pid}/{name}', 'rb') as f:
                    result[name] = fn(f.read(), dictcls=self._dictcls)
            except PermissionError as ex:
                logger.warning(str(ex))
                result[name] = self._dictcls(fn.empty) if isinstance(fn.empty, dict) else fn.empty
        return result

    def get_nodemap(self):
        if 'stat' not in self._proc_file_registry:
            raise RuntimeError('stat file reader is required')

        pids = get_pid_list()
        if self._skip_self:
            pids.remove(os.getpid())

        lookup = {}
        for p in list(pids):
            try:
                lookup[p] = self._read_process_dict(p)
            except FileNotFoundError:
                # Race condition
                pids.remove(p)

        for p in pids:
            node = lookup[p]
            if node['stat']['ppid'] != 0:
                lookup[node['stat']['ppid']].setdefault('children', []).append(node)

        return lookup

    def get_root(self):
        return self.get_nodemap()[1]


def _flatten_hierarchy(node_list):
    """Turn tree node list recursively into a flat list."""

    result = []
    for node in node_list:
        result.append(node)
        result.extend(_flatten_hierarchy(getattr(node, 'children', [])))

    return result

def _flatten_file_keys(node: dict, file_list):
    """Make flat dictionary out of proc file nest dictionary."""

    result = {}
    for file_key, value in node.items():
        if file_key not in file_list:
            continue

        if isinstance(value, dict):
            result.update({f'{file_key}_{k}': v for k, v in value.items()})
        else:
            result[file_key] = value

    return result

def flatten(data, file_list):
    """Make a PID → flat mapping out of a subtree or node list."""

    result = _flatten_hierarchy(data if isinstance(data, list) else [data])
    result = {n['stat']['pid']: _flatten_file_keys(n, file_list) for n in result}
    return list(result.values())
