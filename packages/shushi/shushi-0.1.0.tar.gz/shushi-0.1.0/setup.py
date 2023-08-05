import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = "shushi"
DESCRIPTION = "Minimalist secrets management in Python"
URL = "https://github.com/alexmacniven/shushi"
EMAIL = "macniven.ap@gmail.com"
AUTHOR = "Alex Macniven"
REQUIRES_PYTHON = ">=3.7.0"

# What packages are required for this module to be executed?
REQUIRED = [
    "click",
    "cryptography"
]

# What packages are optional?
EXTRAS = {
    "dev": [
        "pytest",
        "pytest-mock",
        "rope",
        "flake8",
        "coverage",
        "twine"
    ]
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if "README.md" is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package"s __version__.py module as a dictionary.
about = {}
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(here, project_slug, "__version__.py")) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            print('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        print('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        print('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        print('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "shushi=shushi.cli:cli"
        ]
    },
    license="MIT"
)
