from setuptools import setup, find_packages

setup(
    name='ARMP',
    version='0.1',
    packages=find_packages(),
    package_data={
        'ARMP': ['ARMP/data/.keep'],
        'ARMP': ['ARMP/output/.keep'],
        'ARMP': ['ARMP/figure/.keep'],
    },
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'install_ARMP=installation.install:main',
            'ARMP_version=installation.__init__:print_version',  # New entry point
        ],
    },
)

