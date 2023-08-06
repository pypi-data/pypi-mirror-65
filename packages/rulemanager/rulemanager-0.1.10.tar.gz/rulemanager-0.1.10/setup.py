"""

rulemanager :  Copyright 2018-2020, Blake Huber

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

see: https://www.gnu.org/licenses/#GPL

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
contained in the program LICENSE file.

"""

import os
import sys
import platform
import subprocess
import inspect
from shutil import which
from shutil import copy2 as copyfile
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import getpass
from codecs import open
import rulemanager


requires = [
    'boto3>=1.12.1',
    'libtools>=0.3.3',
    'cron-descriptor'
]


_project = 'rulemanager'
_root = os.path.abspath(os.path.dirname(__file__))
_iam_script = 'iam_identities.py'
_rgn_script = 'regions.py'
_comp_fname = 'rulemanager-completion.bash'


def _git_root():
    """Returns root directory of git repository"""
    cmd = 'git rev-parse --show-toplevel 2>/dev/null'
    return subprocess.getoutput(cmd).strip()


def _root_user():
    """
    Checks localhost root or sudo access.  Returns bool
    """
    if os.geteuid() == 0:
        return True
    elif subprocess.getoutput('echo $EUID') == '0':
        return True
    return False


def _user():
    """Returns username of caller"""
    return getpass.getuser()


def _set_pythonpath():
    """
    Temporarily reset PYTHONPATH to prevent home dir = python module home
    """
    os.environ['PYTHONPATH'] = '/'


def create_artifact(object_path, type):
    """Creates post install filesystem artifacts"""
    if type == 'file':
        with open(object_path, 'w') as f1:
            f1.write(sourcefile_content())
    elif type == 'dir':
        os.makedirs(object_path)


def _install_root():
    """Filsystem installed location of program modules"""
    if not _root_user():
        return os.path.abspath(os.path.dirname(rulemanager.__file__))
    return os.path.join(inspect.getsourcefile(setup).split('setuptools')[0], _project)


def module_src():
    """Alt method of finding filsystem location of Python3 modules"""
    bin_path = which('python3.6') or which('python3.7')
    bin = os.path.split(bin_path)[1]
    if 'local' in bin_path:
        return '/usr/local/lib/' + bin + '/site-packages'
    return '/usr/lib/' + bin + '/site-packages'


def os_parityPath(path):
    """
    Converts unix paths to correct windows equivalents.
    Unix native paths remain unchanged (no effect)
    """
    path = os.path.normpath(os.path.expanduser(path))
    if path.startswith('\\'):
        return 'C:' + path
    return path


class PostInstallDevelop(develop):
    """ post-install, development """
    def run(self):
        subprocess.check_call("bash scripts/post-install-dev.sh".split())
        develop.run(self)


class PostInstall(install):
    """
    Summary.

        Postinstall script to place bash completion artifacts
        on local filesystem

    """
    def valid_os_shell(self):
        """
        Summary.

            Validates install environment for Linux and Bash shell

        Returns:
            Success | Failure, TYPE bool

        """
        if platform.system() == 'Windows':
            return False
        elif which('bash'):
            return True
        elif 'bash' in subprocess.getoutput('echo $SHELL'):
            return True
        return False

    def run(self):
        """
        Summary.

            Executes post installation configuration only if correct
            environment detected

        """
        if self.valid_os_shell():

            completion_file = os.path.join(user_home(), '.bash_completion')
            completion_dir = os.path.join(user_home(), '.bash_completion.d')
            config_dir = os.path.join(user_home(), '.config', _project)

            if not os.path.exists(os_parityPath(completion_file)):
                create_artifact(os_parityPath(completion_file), 'file')
            if not os.path.exists(os_parityPath(completion_dir)):
                create_artifact(os_parityPath(completion_dir), 'dir')
            if not os.path.exists(os_parityPath(config_dir)):
                create_artifact(os_parityPath(config_dir), 'dir')

            ## ensure installation of home directory artifacts (data_files) ##

            # bash_completion; (overwrite if exists)
            copyfile(
                os_parityPath(os.path.join('bash', _comp_fname)),
                os_parityPath(os.path.join(completion_dir, _comp_fname))
            )
            # configuration files: excluded file types
            if not os.path.exists(os_parityPath(os.path.join(config_dir, _iam_script))):
                copyfile(
                    os_parityPath(os.path.join('bash', _iam_script)),
                    os_parityPath(os.path.join(config_dir, _iam_script))
                )
            # configuration files: excluded directories
            if not os.path.exists(os_parityPath(os.path.join(config_dir, _rgn_script))):
                copyfile(
                    os_parityPath(os.path.join('bash', _rgn_script)),
                    os_parityPath(os.path.join(config_dir, _rgn_script))
                )
        install.run(self)


class PostInstallRoot(install):
    """
    Summary.

        Postinstall script to place bash completion artifacts
        on local filesystem

    """
    def valid_os_shell(self):
        """
        Summary.

            Validates install environment for Linux and Bash shell

        Returns:
            Success | Failure, TYPE bool

        """
        if platform.system() == 'Windows':
            return False
        elif which('bash'):
            return True
        elif 'bash' in subprocess.getoutput('echo $SHELL'):
            return True
        return False

    def run(self):
        """
        Summary.

            Executes post installation configuration only if correct
            environment detected

        """
        # bash shell + root user
        if self.valid_os_shell():

            completion_dir = '/etc/bash_completion.d'
            config_dir = os.path.join(_install_root(), 'config')

            if not os.path.exists(os_parityPath(config_dir)):
                create_artifact(os_parityPath(config_dir), 'dir')

            ## ensure installation of home directory artifacts (data_files) ##

            # bash_completion; (overwrite if exists)
            copyfile(
                os_parityPath(os.path.join('bash', _comp_fname)),
                os_parityPath(os.path.join(completion_dir, _comp_fname))
            )
            # configuration files: excluded file types
            if not os.path.exists(os_parityPath(os.path.join(config_dir,  _iam_script))):
                copyfile(
                    os_parityPath(os.path.join('bash', _iam_script)),
                    os_parityPath(os.path.join(config_dir, _iam_script))
                )
            # configuration files: excluded directories
            if not os.path.exists(os_parityPath(os.path.join(config_dir, _rgn_script))):
                copyfile(
                    os_parityPath(os.path.join('bash', _rgn_script)),
                    os_parityPath(os.path.join(config_dir, _rgn_script))
                )
        install.run(self)


def preclean(dst):
    if os.path.exists(dst):
        os.remove(dst)
    return True


def read(fname):
    basedir = os.path.dirname(sys.argv[0])
    return open(os.path.join(basedir, fname)).read()


def sourcefile_content():
    sourcefile = """
    for bcfile in ~/.bash_completion.d/* ; do
        [ -f "$bcfile" ] && . $bcfile
    done\n
    """
    return sourcefile


def user_home():
    """Returns os specific home dir for current user"""
    try:
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            # Linux or BSD Unix (Mac)
            return os.path.expanduser('~') or os.environ.get('HOME')

        elif platform.system() == 'Windows':
            username = os.getenv('username')
            return 'C:\\Users\\' + username

        elif platform.system() == 'Java':
            print('Unable to determine home dir, unsupported os type')
            sys.exit(1)
    except OSError as e:
        raise e


# branch install based on user priviledge level

if _root_user():

    setup(
        name=_project,
        version=rulemanager.__version__,
        description='Manage Amazon CloudWatch rules via cli',
        long_description=read('DESCRIPTION.rst'),
        url='https://bitbucket.org/the_organization/rulemanager',
        author=rulemanager.__author__,
        author_email=rulemanager.__email__,
        license='GPL-3.0',
        classifiers=[
            'Topic :: Software Development :: Build Tools',
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: POSIX :: Linux',
        ],
        keywords='Amazon AWS ec2 cloudwatch rules events',
        packages=find_packages(exclude=['assets', 'docs', 'reports', 'scripts', 'tests']),
        include_package_data=True,
        install_requires=requires,
        python_requires='>=3.6, <4',
        cmdclass={
            'install': PostInstallRoot
        },
        data_files=[
            (
                os.path.join('/etc/bash_completion.d'),
                [os.path.join('bash', _comp_fname)]
            ),
            (
                os.path.join(_install_root(), 'config'),
                [os.path.join('bash', _iam_script), os.path.join('bash', _rgn_script)]
            )
        ],
        entry_points={
            'console_scripts': [
                'rulemanager=rulemanager.cli:init'
            ]
        },
        zip_safe=False
    )

else:

    # non-priviledged user

    setup(
        name=_project,
        version=rulemanager.__version__,
        description='Manage Amazon CloudWatch rules via cli',
        long_description=read('DESCRIPTION.rst'),
        url='https://bitbucket.org/the_organization/rulemanager',
        author=rulemanager.__author__,
        author_email=rulemanager.__email__,
        license='GPL-3.0',
        classifiers=[
            'Topic :: Software Development :: Build Tools',
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: POSIX :: Linux',
        ],
        keywords='Amazon AWS ec2 cloudwatch rules events',
        packages=find_packages(exclude=['assets', 'docs', 'reports', 'scripts', 'tests']),
        include_package_data=True,
        install_requires=requires,
        python_requires='>=3.6, <4',
        cmdclass={
            'install': PostInstall
        },
        data_files=[
            (
                os.path.join(user_home(), '.bash_completion.d'),
                [os.path.join('bash', _comp_fname)]
            ),
            (
                os.path.join(_install_root(), 'config'),
                [os.path.join('bash', _iam_script), os.path.join('bash', _rgn_script)]
            )
        ],
        entry_points={
            'console_scripts': [
                'rulemanager=rulemanager.cli:init'
            ]
        },
        zip_safe=False
    )
