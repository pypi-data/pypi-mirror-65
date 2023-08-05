import os
from setuptools import setup
from collectors import __version__
from setuptools import find_packages

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    # Meta data
    name='infra-agent',
    version=__version__,
    author='Muhammad Azhar',
    author_email='azhar@contentstudio.io',
    maintainer='Muhammad Azhar',
    maintainer_email='azhar@contentstudio.io',
    url='https://contentstudio.io',
    description='Python package for infastructure agent.',
    # long_description=open(os.path.join(ROOT, 'README.md')).read(),
    license='MIT License',
    # Package files
    packages=find_packages(),
    include_package_data=True,
    # Dependencies
    install_requires=[
        'requests',
        'uptime',
        'distro',
        'netifaces==0.10.9',
        'psutil',
    ],
    extras_require={
        'full': ['urllib3', 'certifi'],
    },
    entry_points={
        'console_scripts': [
            'infra-agent = agent.agent:main',
        ],
    },
    test_suite='nose.collector'
)
