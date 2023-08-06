import os

import setuptools

README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
REQUIREMENTS_FILE = os.path.join(os.path.dirname(__file__), 'requirements.txt')
VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
DEFAULT_VERSION = '0.0.1'


def get_description():
    # When running tests using tox, README.md is not found
    desc = ''
    try:
        with open(README_FILE) as file:
            desc = file.read()
    except FileNotFoundError:
        pass

    return desc


def get_version():
    with open(VERSION_FILE) as f:
        git_version = f.read().strip()
        if not git_version:
            raise Exception('Versão não definida')
        git_version = git_version.split('-')
        version = git_version[0]
        if len(git_version) > 1:
            version += '.post' + git_version[1]
        return version


def get_requirements():
    with open(REQUIREMENTS_FILE) as f:
        requirements = f.read().splitlines()

    return requirements


setuptools.setup(
    name="congressy-sdk",
    version=get_version(),
    author="Hugo Seabra",
    author_email="infra@congressy.com",
    description="A python client for v1 of Congressy API",
    long_description=get_description(),
    install_requires=get_requirements(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/congressy/congressy-sdk-python",
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
    ],
    keywords='congressy api v1 client wrapper event platform',
    python_requires='>=3.5',
)
