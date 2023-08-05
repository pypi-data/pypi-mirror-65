from setuptools import find_packages, setup, Command
import os
import sys
from shutil import rmtree

NAME = "gsecrets"
here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, NAME, "__version__.py")) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPi via Twine...")
        os.system("twine upload dist/*")

        sys.exit()

setup(
    name="gsecrets",
    version=about["__version__"],
    description=about["__description__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(),
    license=about["__license__"],
    install_requires=[
        "click==7.0",
        "google-api-python-client==1.7.11",
        "google-cloud-storage==1.19.1",
        "ndg-httpsclient==0.5.1",
        "pyasn1==0.4.8",
        "pyopenssl==19.1.0",
        "requests==2.23.0",
    ],
    entry_points={"console_scripts": ["gsecrets = gsecrets.cli:cli"]},
    cmdclass={"upload": UploadCommand},
)
