import os
import logging
from setuptools import setup, find_packages


try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
except ImportError as e:
    logging.warning("unable to import pypandoc. {0}".format(str(e)))
    with open("README.md", "r") as f:
        long_description = f.read()


here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, "errorship", "__version__.py"), "r") as f:
#     x = f.read()
#     y = x.replace("about = ", "")
#     about = ast.literal_eval(y)

about = {
    "__title__": "errorship",
    "__version__": "v0.0.7-beta",
    "__description__": "Send exceptions to datadog.",
    "__url__": "https://errorship.com/",
    "__author__": "errorship.com",
    "__author_email__": "errorship.com@gmail.com",
    "__license__": "https://gitlab.com/errorship/errorship_python/-/blob/master/LICENSE",
    "long_description": long_description,
}


setup(
    name=about["__title__"],
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=about["__version__"],
    description=about["__description__"],
    long_description=about["long_description"],
    # The project's main homepage.
    url=about["__url__"],
    # Author details
    author=about["__author__"],
    author_email=about["__author_email__"],
    # Choose your license
    license=about["__license__"],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        # Pick your license as you wish (should match "license" above)
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    # What does your project relate to?
    keywords="errorship, errors, exceptions, datadog, error tracker, error tracking",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(
        exclude=[
            "documentation",
            "*examples*",
            "*tests*",
            ".github",
            ".gitlab",
            "documentation/sphinx-docs",
            "sphinx-build",
        ]
    ),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test_py3,test_py2,examples]
    extras_require={
        "dev": [
            "twine==3.1.1",
            "wheel==0.33.6",
            "Sphinx==2.2.2",
            "pypandoc==1.5",
            "sphinx-autodoc-typehints==1.10.3",
            "sphinx-rtd-theme==0.4.3",
        ],
        "test_py3": ["flake8", "pylint", "black", "bandit", "mypy", "pytype", "coverage", "mock"],
        "test_py2": ["flake8", "pylint", "coverage", "mock"],
        "examples": ["django==1.11", "flask==1.1"],  # we need the ones that support both py2 & py3
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)

# python packaging documentation:
# 1. https://python-packaging.readthedocs.io/en/latest/index.html
# 2. https://python-packaging-user-guide.readthedocs.io/tutorials/distributing-packages
# a) pip install wheel twine
# b) pip install -e .
# c) python setup.py sdist
# d) python setup.py bdist_wheel
# e) DONT use python setup.py register and python setup.py upload. They use http
# f) twine upload dist/* -r testpypi
# g) pip install -i https://testpypi.python.org/pypi <package name>
# h) twine upload dist/*   # prod pypi
# i) pip install <package name>
# pip install -e .[dev,test_py3,test_py2,examples]
