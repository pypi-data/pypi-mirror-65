import pathlib
from setuptools import setup

#https://realpython.com/pypi-publish-python-package/#reader-comments
# The directory containing this file

# bumpversion --current-version 1.15.0 minor setup.py uPyExplorer/__init__.py
# python3 setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# twine upload dist/*

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="uPyExplorer",
    version="1.15.0",
    description="Explorer for Micropython Device",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/RetepRelleum/uPyExplorer",
    author="Real Python",
    author_email="retep.relleum@bluewin.ch",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["uPyExplorer"],
    include_package_data=True,
    install_requires=["pyserial"],
    entry_points={
        "console_scripts": [
            "uPyExplorer=uPyExplorer.__main__:main",
        ]
    },
)



