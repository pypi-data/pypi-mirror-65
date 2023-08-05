"""
Pykrete module build script
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
# pylint: disable=wrong-import-order
import src_appender
from logging.config import fileConfig
from setuptools import setup, find_packages
from pykrete.packages import PythonPackage
from pykrete.distrib import TwineCommand, BuildGitSshTag
from pykrete.distrib.pylint import SelfTestCommand, ProjectTestCommand


fileConfig('loggingrc')
src_appender.print_path()
PACKAGE = PythonPackage('pykrete')
print(f'Handling pip package: {PACKAGE}')
setup(
    name='pykrete',
    version=PACKAGE.version,
    license='MIT',
    author='Shai A. Bennathan',
    author_email='shai.bennathan@intel.com',
    description='Build script foundation',
    long_description=PACKAGE.long_description,
    long_description_content_type='text/markdown',
    url='http://ait-tool-center.iil.intel.com/',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
    cmdclass={
        'pylint_self': SelfTestCommand,
        'pylint': ProjectTestCommand,
        'twine': TwineCommand,
        'build_git_ssh_tag': BuildGitSshTag
    },
)
