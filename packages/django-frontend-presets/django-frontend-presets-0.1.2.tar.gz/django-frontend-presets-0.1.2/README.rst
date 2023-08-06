=============================
Django Frontend Presets
=============================

.. image:: https://badge.fury.io/py/django-frontend-presets.svg
    :target: https://badge.fury.io/py/django-frontend-presets

.. image:: https://travis-ci.org/mikemenard/django-frontend-presets.svg?branch=master
    :target: https://travis-ci.org/mikemenard/django-frontend-presets

.. image:: https://codecov.io/gh/mikemenard/django-frontend-presets/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mikemenard/django-frontend-presets

Django frontend presets provide a command line that allow you to rapidly swap the front-end scaffolding for the application.

Documentation
-------------

The full documentation is at https://django-frontend-presets.readthedocs.io.

Quickstart
----------

Install Django Frontend Presets::

    pip install django-frontend-presets

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_frontend_presets.apps.DjangoFrontendPresetsConfig',
        ...
    )

Add Django Frontend Presets's URL patterns:

.. code-block:: python

    from django_frontend_presets import urls as django_frontend_presets_urls


    urlpatterns = [
        ...
        url(r'^', include(django_frontend_presets_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
