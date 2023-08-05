import re
from setuptools import find_packages, setup

# get version from himalaya/__init__.py
with open('himalaya/__init__.py') as f:
    infos = f.readlines()
for line in infos:
    if "__version__" in line:
        match = re.search(r"__version__ = '([^']*)'", line)
        __version__ = match.groups()[0]

if __name__ == "__main__":
    setup(
        name='himalaya',
        long_description=open('README.rst').read(),
        maintainer="Tom Dupre la Tour",
        maintainer_email="tom.dupre-la-tour@m4x.org",
        description="Coming soon",
        license='BSD (3-clause)',
        version=__version__,
        packages=find_packages(),
    )
