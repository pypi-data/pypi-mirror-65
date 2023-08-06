import re

from setuptools import find_packages, setup

with open('iprpc/__init__.py', encoding='utf-8') as ver_file:
    ver = re.compile(r"__version__\s*=\s*'(.*?)'.*", re.S).match(
        ver_file.read()
    )
    if ver is not None:
        version = ver.group(1)
    else:
        version = '0.0.0'

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('requirements.txt', encoding='utf-8') as requirements_file:
    requirements = requirements_file.read()

with open('requirements_aioapp.txt', encoding='utf-8') as requirements_file:
    requirements_aioapp = requirements_file.read()

with open('requirements_aiohttp.txt', encoding='utf-8') as requirements_file:
    requirements_aiohttp = requirements_file.read()

with open('requirements_dev.txt', encoding='utf-8') as requirements_dev_file:
    test_requirements = requirements_dev_file.read()
    test_requirements = test_requirements.replace(
        '-r requirements.txt', requirements
    )
    test_requirements = test_requirements.replace(
        '-r requirements_aiohttp.txt', requirements_aiohttp
    )
    test_requirements = test_requirements.replace(
        '-r requirements_aioapp.txt', requirements_aioapp
    )

setup(
    name='iprpc',
    version=version,
    description="InPlat JSON RPC library",
    long_description=readme,
    author="Konstantin Stepanov",
    url='https://gitlab.app.ipl/inplat/iprpc/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=list(filter(lambda a: a, requirements.split('\n'))),
    extras_require={
        'aioapp': list(filter(lambda a: a, requirements_aioapp.split('\n'))),
        'aiohttp': list(filter(lambda a: a, requirements_aiohttp.split('\n'))),
    },
    license="Apache License 2.0",
    zip_safe=False,
    keywords='iprpc',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=list(filter(lambda a: a, test_requirements.split('\n'))),
    python_requires='~=3.6',
)
