import os
import shutil

from .Preset import Preset
from ..utils import root_path, applications_path, stubs_path


class Init(Preset):

    def install(self):
        self.delete_default_frontend()
        self.setup_frontend()

    def update_package_list(self, packages):
        pass

    def delete_default_frontend(self):
        self.delete_paths((
            applications_path('static'),
            applications_path('templates'),
            root_path('templates'),
            root_path('static'),
            root_path('node_modules'),
            root_path('locale'),
            root_path('resources'),
            root_path('package.json'),
            root_path('package-lock.json'),
            root_path('gulpfile.js'),
            root_path('yarn.lock'),
            root_path('webpack.mix.js'),
            root_path('npm-debug.log'),
            root_path('yarn-debug.log'),
            root_path('yarn-error.log'),
            root_path('mix-manifest.json'),
        ))

    def setup_frontend(self):
        shutil.copytree(stubs_path('init', 'resources'), root_path('resources'))
        shutil.copy(stubs_path('init', 'package.json'), root_path())
        shutil.copy(stubs_path('init', 'webpack.mix.js'), root_path())

    @staticmethod
    def check_installation():
        directories = (
            root_path('resources'),
            root_path('resources', 'locale'),
            root_path('resources', 'static'),
            root_path('resources', 'templates'),
            root_path('package.json'),
            root_path('webpack.mix.js'),
        )

        for directory in directories:
            if not os.path.exists(directory):
                return False
        return True
