import shutil

from .Preset import Preset
from ..utils import root_path, stubs_path


class Vue(Preset):
    def install(self):
        super().ensure_component_dir_exists()
        super().update_webpack_config(stub_dir='init')
        super().update_packages()
        self.update_components()
        self.update_bootstrapping()

    def update_package_list(self, packages):
        packages['vue'] = '^2.5.17'
        packages.pop('@babel/preset-react', None)
        packages.pop('react', None)
        packages.pop('react-dom', None)
        return packages

    def update_components(self):
        self.delete_paths((
            root_path('resources', 'static', 'js', 'components', 'Example.js'),
            root_path('resources', 'static', 'js', 'components', 'ExampleComponent.vue'),
        ))
        shutil.copy(stubs_path('vue', 'ExampleComponent.vue'), root_path('resources', 'static', 'js', 'components'))

    def update_bootstrapping(self):
        self.delete_paths((
            root_path('resources', 'static', 'js', 'app.js'),
        ))
        shutil.copy(stubs_path('vue', 'app.js'), root_path('resources', 'static', 'js'))
