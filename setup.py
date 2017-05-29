# flake8: noqa
from typing import Dict

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def get_file_content(file_name):
    with open(os.path.join(here, file_name), encoding='utf-8') as f:
        return f.read()


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'docs':
    os.system('cd docs/ && make html && cd ..')
    sys.exit()

about = {}  # type: Dict[str, str]
exec(get_file_content(os.path.join(here, 'smsc', '__version__.py')), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=get_file_content('README.rst') + '\n\n' + get_file_content('HISTORY.rst'),
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    classifiers=(
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries",
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ),
    keywords='smsc.ru smsc sms',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_file_content('requirements.txt'),
    tests_require=get_file_content('requirements_test.txt'),
    setup_requires=['pytest-runner'],
    test_suite='tests',
)
