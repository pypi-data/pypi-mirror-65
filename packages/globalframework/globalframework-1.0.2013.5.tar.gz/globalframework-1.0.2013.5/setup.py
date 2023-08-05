import io
import re
import sys

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)


if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of GlobalFramework requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

with io.open("globalframework/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="globalframework",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    version=version,
    packages=find_packages(exclude=["*.test.*", "*.test"]),
    include_package_data=True,
    install_requires=[
        "wheel",
        "cryptography==2.7.0",
        "psycopg2==2.8.4",
        "pyodbc==4.0.26",
        "pymysql==0.9.3",
        "mysql-connector-python==8.0.16",
        "pymemcache==2.2.0",
        "celery==4.3.0",
    ],
)
