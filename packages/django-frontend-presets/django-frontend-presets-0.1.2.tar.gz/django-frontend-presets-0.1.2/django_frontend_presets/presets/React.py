import shutil

from .Preset import Preset
from ..utils import root_path, stubs_path


class React(Preset):
    def install(self):
        super().ensure_component_dir_exists()
        super().update_packages()
        super().update_webpack_config(stub_dir='react')
        self.update_bootstrapping()
        self.update_component()

    def update_package_list(self, packages):
        packages['@babel/preset-react'] = '^7.0.0'
        packages['react'] = '^16.2.0'
        packages['react-dom'] = '^16.2.0'
        packages.pop('vue', None)
        packages.pop('vue-template-compiler', None)
        return packages

    def update_bootstrapping(self):
        self.delete_paths((
            root_path('resources', 'static', 'js', 'app.js'),
        ))
        shutil.copy(stubs_path('react', 'app.js'), root_path('resources', 'static', 'js'))

    def update_component(self):
        self.delete_paths((
            root_path('resources', 'static', 'js', 'components', 'Example.js'),
            root_path('resources', 'static', 'js', 'components', 'ExampleComponent.vue'),
        ))
        shutil.copy(stubs_path('react', 'Example.js'), root_path('resources', 'static', 'js', 'components'))
