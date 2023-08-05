"""Setup for PyPi package."""

import os
import pathlib

import setuptools

os.environ['SHTUKA_SETUP'] = str(True)
import shtuka  # noqa, isort:skip

HOME_URL = 'https://github.com/stasbel/shtuka'
CONFIGS_DIR = 'configs'

# https://github.com/stasbel/dotfiles/wiki/Python-Linters
extras_require = dict(
    format=['isort', 'black'],
    lint=[
        'vulture',
        'flake8',
        'pep8-naming',
        'flake8-bugbear',
        'flake8-docstrings',
        # This is quite unstable and pure tested at the moment.
        # 'darglint',
        'flake8-pytest-style',
        'flake8-eradicate',
        'flake8-comprehensions',
        'flake8-logging-format',
        'flake8-builtins',
        'mypy',
    ],
    test=[
        'pytest',
        # https://github.com/Teemu/pytest-sugar/issues/187
        # 'pytest-sugar',
        'pytest-xdist',
        'pytest-cov',
        'pytest-doctest-ellipsis-markers',
    ],
)
extras_require['dev'] = sum(
    (extras_require[k] for k in ['format', 'lint', 'test']), ['tox']
)
extras_require['all'] = sum(extras_require.values(), [])


# https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata
setuptools.setup(
    name='shtuka',
    version=shtuka.__version__,
    url=HOME_URL,
    download_url=HOME_URL,
    project_urls={
        "Source Code": HOME_URL,
        "Bug Tracker": f'{HOME_URL}/issues',
    },
    author='Stanislav Beliaev',
    author_email='stasbelyaev96@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    license='MIT',
    description='Neat and tidy configs gadget with methods on steroids 🔥',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    keywords=['yaml', 'json', 'config', 'tool', 'dict'],
    # https://packaging.python.org/discussions/install-requires-vs-requirements/#requirements-files
    install_requires=['PyYAML'],
    extras_require=extras_require,
    python_requires='>=3.6',
    include_package_data=True,
    packages=setuptools.find_packages(exclude=['tests']),
    data_files=[
        (CONFIGS_DIR, [str(f) for f in pathlib.Path(CONFIGS_DIR).glob('*')])
    ],
)
