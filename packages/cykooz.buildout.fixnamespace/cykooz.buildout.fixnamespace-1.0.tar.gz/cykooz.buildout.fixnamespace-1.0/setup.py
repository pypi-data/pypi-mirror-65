# encoding: utf-8
import os
import sys

from setuptools import setup, find_packages, findall

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.append(HERE)

import version


def find_package_data():
    ignore_ext = {'.py', '.pyc', '.pyo'}
    base_package = 'cykooz'
    package_data = {}
    root = os.path.join(HERE, base_package)
    for path in findall(root):
        if path.endswith('~'):
            continue
        ext = os.path.splitext(path)[1]
        if ext in ignore_ext:
            continue

        # Find package name
        package_path = os.path.dirname(path)
        while package_path != root:
            if os.path.isfile(os.path.join(package_path, '__init__.py')):
                break
            package_path = os.path.dirname(package_path)
        package_name = package_path[len(HERE) + 1:].replace(os.path.sep, '.')

        globs = package_data.setdefault(package_name, set())
        data_path = path[len(package_path) + 1:]
        data_glob = os.path.join(os.path.dirname(data_path), '*' + ext)
        globs.add(data_glob)
    for key, value in package_data.items():
        package_data[key] = list(value)
    return package_data


README = open(os.path.join(HERE, 'README.rst')).read()
CHANGES = open(os.path.join(HERE, 'CHANGES.rst')).read()


setup(
    name='cykooz.buildout.fixnamespace',
    version=version.get_version(),
    description=u'A zc.buildout extension changes value of NAMESPACE_PACKAGE_INIT constant from setuptools',
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/x-rst',
    keywords='development build',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Buildout',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    author='Kirill Kuzminykh',
    author_email='cykooz@gmail.com',
    url='https://github.com/Cykooz/cykooz.buildout.fixnamespace',
    license='MIT',
    package_dir={'': '.'},
    packages=find_packages(),
    package_data=find_package_data(),
    zip_safe=False,
    extras_require={
        'test': [
            'pytest',
            'zc.buildout [test]'
        ],
    },
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    entry_points={
        'zc.buildout.extension':
        [
            'default = cykooz.buildout.fixnamespace.extension:extension',
        ],
        'console_scripts': [
            'runtests = cykooz.buildout.fixnamespace.runtests:runtests [test]',
        ]
    },
)
