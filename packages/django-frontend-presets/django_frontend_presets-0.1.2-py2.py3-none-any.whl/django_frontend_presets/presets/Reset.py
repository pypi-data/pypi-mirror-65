import shutil

from .Preset import Preset
from ..utils import root_path, stubs_path


class Reset(Preset):
    def install(self):
        self.update_bootstrapping()
        super().update_webpack_config(stub_dir='init')
        super().update_packages()

    def update_package_list(self, packages):
        package_to_delete = (
            'bootstrap',
            'jquery',
            'popper.js',
            'vue',
            'vue-template-compiler',
            '@babel/preset-react',
            'react',
            'react-dom',
        )

        for name in package_to_delete:
            if name in packages.keys():
                del packages[name]
        return packages

    def update_bootstrapping(self):
        self.delete_paths((
            root_path('resources', 'static', 'js', 'components'),
            root_path('resources', 'static', 'js', 'dist', 'app.js'),
            root_path('resources', 'static', 'js', 'app.js'),
            root_path('resources', 'static', 'js', 'bootstrap.js'),
            root_path('resources', 'static', 'sass', 'app.scss'),
            root_path('resources', 'static', 'sass', '_variables.scss'),
            root_path('resources', 'static', 'css', 'app.css'),
            root_path('node_modules'),
        ))
        shutil.copy(stubs_path('init', 'resources', 'static', 'js', 'app.js'), root_path('resources', 'static', 'js'))
        shutil.copy(
            stubs_path('init', 'resources', 'static', 'js', 'bootstrap.js'),
            root_path('resources', 'static', 'js')
        )
        shutil.copy(
            stubs_path('init', 'resources', 'static', 'sass', 'app.scss'),
            root_path('resources', 'static', 'sass')
        )
