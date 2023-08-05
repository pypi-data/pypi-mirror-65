#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-pycharm-workspace',
        version = '0.1.3',
        description = 'PyBuilder PyCharm Workspaces Plugin',
        long_description = 'External plugin for PyBuilder integration with PyCharm',
        author = 'Diego BM',
        author_email = 'diegobm92@gmail.com',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/yeuk0/pybuilder-pycharm-workspace',
        scripts = [],
        packages = [
            'pybuilder_pycharm_workspace',
            'pybuilder_pycharm_workspace.resources'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
