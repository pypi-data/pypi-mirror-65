# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='release_info',
    version_info=(0, 1, 2),
    __version__='0.1.2',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='automatically updated python release information',
    keywords='pypi statistics',
    entry_points='python_release_info=release_info.__main__:main',
    # entry_points=None,
    license='Copyright Ruamel bvba 2007-2020',
    since=2020,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    universal=True,
    install_requires=[],
    tox=dict(
        env='3',
    ),
    print_allowed=True,
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']


def release_info():
    from .release_info import release_info as ri  # NOQA

    return ri
