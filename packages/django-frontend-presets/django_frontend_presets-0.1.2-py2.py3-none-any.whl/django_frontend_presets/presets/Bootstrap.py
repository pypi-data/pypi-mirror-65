import shutil

from .Preset import Preset
from ..utils import root_path, stubs_path


class Bootstrap(Preset):

    def install(self):
        super().update_packages()
        self.update_sass()
        self.update_bootstrapping()

    def update_package_list(self, packages):
        packages['bootstrap'] = '^4.0.0'
        packages['jquery'] = '^3.2'
        packages['popper.js'] = '^1.12'
        return packages

    def update_sass(self):
        self.delete_paths((
            root_path('resources', 'static', 'sass', 'app.scss'),
            root_path('resources', 'static', 'sass', '_variables.scss'),
        ))
        shutil.copy(
            stubs_path('bootstrap', 'app.scss'),
            root_path('resources', 'static', 'sass')
        )
        shutil.copy(
            stubs_path('bootstrap', '_variables.scss'),
            root_path('resources', 'static', 'sass')
        )

    def update_bootstrapping(self):
        self.delete_paths((
            root_path('resources', 'static', 'js', 'bootstrap.js'),
        ))
        shutil.copy(stubs_path('bootstrap', 'bootstrap.js'), root_path('resources', 'static', 'js'))
