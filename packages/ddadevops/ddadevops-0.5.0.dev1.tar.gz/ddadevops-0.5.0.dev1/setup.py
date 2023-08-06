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
        name = 'ddadevops',
        version = '0.5.0.dev1',
        description = 'tools to support builds combining gopass, terraform, dda-pallet, aws & hetzner-cloud',
        long_description = '',
        author = 'meissa GmbH',
        author_email = 'buero@meissa-gmbh.de',
        license = 'Apache Software License',
        url = 'https://github.com/DomainDrivenArchitecture/dda-devops-build',
        scripts = [],
        packages = ['ddadevops'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Operating System :: POSIX :: Linux',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing'
        ],
        entry_points = {},
        data_files = [],
        package_data = {
            'ddadevops': ['LICENSE', 'src/main/resources/terraform/*']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '!=3.0,!=3.1,!=3.2,!=3.3,!=3.4,<3.9,>=2.7',
        obsoletes = [],
    )
