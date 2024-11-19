from setuptools import find_packages, setup

setup(
    name="ARMP",
    version="0.1",
    packages=find_packages(),
    package_data={
        "ARMP": [
            "params/config.in",
            "data/*.in",
            ".keep",
            "output/.keep",
            "figure/.keep",
        ],
    },
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "install_ARMP=installation.install:main",
            "ARMP_version=installation.__init__:print_version",
        ],
    },
)
