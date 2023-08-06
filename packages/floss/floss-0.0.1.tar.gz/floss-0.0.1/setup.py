import os
import setuptools

THISDIR = os.path.abspath(os.path.dirname(__file__))


def long_desc() -> str:
    with open(os.path.join(THISDIR, "README.rst"), "r") as f:
        return f.read()


setuptools.setup(
    name="floss",
    version="0.0.1",
    author="Jason Fried",
    author_email="me@jasonfried.info",
    description="a LibCST based linting framework",
    long_description=long_desc(),
    keywords="linter flake8 pyflakes pylint lint libcst",
    packages=setuptools.find_packages(),
    zip_safe=True,
    python_requires=">=3.7",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)

