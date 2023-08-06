import abc
import collections
import json
import os
import shutil
from typing import Iterable

from ..utils import root_path, stubs_path


class Preset(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def install(self):
        pass

    @abc.abstractmethod
    def update_package_list(self, packages):
        pass

    def delete_paths(self, paths: Iterable):
        for item in paths:
            if os.path.exists(item):
                if os.path.isfile(item):
                    os.unlink(item)
                if os.path.isdir(item):
                    shutil.rmtree(item, ignore_errors=True)

    def update_packages(self, dev=True):
        if not os.path.exists(root_path('package.json')):
            return

        config_key = 'devDependencies' if dev else 'dependencies'

        with open(root_path('package.json'), 'r+') as file:
            packages = json.load(file)

            if config_key not in packages:
                packages[config_key] = []

            packages[config_key] = collections.OrderedDict(
                sorted(self.update_package_list(packages[config_key]).items())
            )

            file.seek(0)
            json.dump(packages, file, indent=4)
            file.truncate()

        self.delete_paths((
            root_path('yarn.lock'),
            root_path('package-lock.json'),
            root_path('node_modules'),
        ))

    def update_webpack_config(self, stub_dir):
        self.delete_paths(
            (root_path('webpack.mix.js'),)
        )
        shutil.copy(stubs_path(stub_dir, 'webpack.mix.js'), root_path())

    def ensure_component_dir_exists(self):
        components_path = root_path('resources', 'static', 'js', 'components')
        if not os.path.exists(components_path):
            os.mkdir(components_path)
