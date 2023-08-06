import subprocess


__all__ = 'evaluate',


def evaluate(var_cmd_list):
    script = []
    var_set = set()
    for var_name, command in var_cmd_list:
        var_set.add(var_name)
        script.append(f'{var_name}=$({command})')
        script.append(f'export {var_name}')

    script.append('env')
    env = subprocess.check_output('\n'.join(script), shell=True, encoding='utf-8')

    result = {}
    for l in env.splitlines():
        k, v = l.split('=', 1)
        if k in var_set:
            result[k] = v

    return result
