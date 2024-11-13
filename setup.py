from setuptools import setup, find_packages

setup(
    name='ARMP',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'install_ARMP=installation.install:main',
            'ARMP_version=installation.__init__:print_version',  # New entry point
        ],
    },
)

