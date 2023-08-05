from setuptools import setup, find_packages


PACKAGE = "pg_tasks_queue"
NAME = "pg-task-queue"
DESCRIPTION = "Python asinc task system with postgres database"
AUTHOR = "Alex V. Smith"
URL = "https://gitlab.com/cryptoner_dev/tasks_system"
AUTHOR_EMAIL = "smith.it.interface@gmail.com"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    url=URL,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    packages=find_packages(exclude=["tests.*", "tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        'psycopg2',
        'pandas',
    ],
    include_package_data=True,
    zip_safe=False,
)