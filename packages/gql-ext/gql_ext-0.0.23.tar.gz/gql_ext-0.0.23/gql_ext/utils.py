import glob
import json
import os
from abc import ABC, abstractmethod
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from typing import List

import yaml


def parse_conf(path: str) -> dict:
    if not (path.endswith('.json') or path.endswith('.yaml')):
        path = f'{path}.*'
    file_path = glob.glob(path)
    if len(file_path) != 1:
        raise RuntimeError(f'It is impossible to uniquely identify the file {file_path}')
    file_path = file_path[0]

    if file_path.endswith('.json'):
        with open(file_path) as f:
            return json.load(f)

    if file_path.endswith('.yaml'):
        with open(file_path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    raise RuntimeError('Unknown format for config file. Only JSON and YAML supported')


def import_from_module(method: str):
    module = method[:method.rfind('.')]
    method_name = method.split('.')[-1]
    module = import_module(module)
    if not hasattr(module, method_name):
        raise RuntimeError(f'{method_name} is not found in {module}')
    return getattr(module, method_name)


def import_by_full_path(path: str):
    spec = spec_from_file_location("module", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resolve_paths(paths: List) -> List:
    res = []

    for path_ in paths:
        if os.path.isfile(path_):
            res.append(path_)
        else:
            for path, dirs, files in os.walk(path_):
                for file in files:
                    res.append(f'{path}/{file}')
    return res


class ScalarDefinition(ABC):
    @abstractmethod
    def coerce_output(self, value):
        pass

    @abstractmethod
    def coerce_input(self, value):
        pass
