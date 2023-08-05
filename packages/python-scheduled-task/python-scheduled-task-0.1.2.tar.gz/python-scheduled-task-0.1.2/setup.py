# coding: utf-8


import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='python-scheduled-task',
    version='0.1.2',
    description='Python Scheduled Task',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Li Shunan',
    author_email='lishunan246@gmail.com',
    packages=['ScheduledTask'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        'Operating System :: POSIX',
    ],
    install_requires=["crontab", "six"],

)
