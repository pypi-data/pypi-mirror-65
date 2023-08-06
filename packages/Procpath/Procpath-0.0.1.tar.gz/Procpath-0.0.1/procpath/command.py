import json
import string
import time

from . import proctree, procfile, procrec, shell

try:
    import jsonpyth
except ImportError:
    jsonpyth = None


__all__ = 'CommandError', 'query', 'record', 'watch'


class CommandError(Exception):
    """Generic command error."""


def query(file_list, output_file, delimiter=None, indent=None, query=None):
    if query and not jsonpyth:
        raise CommandError('Cannot execute query, jsonpyth is not installed')

    readers = {k: v for k, v in procfile.registry.items() if k in file_list}
    tree = proctree.Tree(readers)
    result = tree.get_root()

    if query:
        try:
            result = jsonpyth.jsonpath(result, query, always_return_list=True)
        except jsonpyth.JsonPathSyntaxError as ex:
            raise CommandError(str(ex)) from ex

    if delimiter:
        result = delimiter.join(map(str, result))
    else:
        result = json.dumps(result, indent=indent, ensure_ascii=False)

    output_file.write(result)
    output_file.write('\n')


def record(
    file_list, database_file, interval, environment=None, query=None, recnum=None, reevalnum=None
):
    if query and not jsonpyth:
        raise CommandError('Cannot execute query, jsonpyth is not installed')

    readers = {k: v for k, v in procfile.registry.items() if k in file_list}
    tree = proctree.Tree(readers)

    count = 1
    with procrec.SqliteStorage(database_file, file_list) as store:
        while True:
            if query and environment and (count == 1 or reevalnum and count % reevalnum == 0):
                query = string.Template(query).safe_substitute(shell.evaluate(environment))

            result = tree.get_root()
            if query:
                try:
                    result = jsonpyth.jsonpath(result, query, always_return_list=True)
                except jsonpyth.JsonPathSyntaxError as ex:
                    raise CommandError(str(ex)) from ex

            store.record(proctree.flatten(result, file_list))

            count += 1
            if recnum and count > recnum:
                break

            time.sleep(interval)
