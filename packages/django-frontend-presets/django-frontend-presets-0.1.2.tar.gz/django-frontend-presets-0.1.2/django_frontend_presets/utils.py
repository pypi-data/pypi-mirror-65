import os

from django.conf import settings

from .settings import STUBS_DIR


def get_project_root():
    base_dir = getattr(settings, 'BASE_DIR', None)
    root_dir = getattr(settings, 'ROOT_DIR', None)

    return root_dir if root_dir else base_dir


def root_path(*args):
    return os.path.join(get_project_root(), *args)


def applications_path(*args):
    if not hasattr(settings, 'APPS_DIR'):
        return root_path(*args)
    return os.path.join(settings.APPS_DIR, *args)


def stubs_path(*args):
    return os.path.join(STUBS_DIR, *args)
