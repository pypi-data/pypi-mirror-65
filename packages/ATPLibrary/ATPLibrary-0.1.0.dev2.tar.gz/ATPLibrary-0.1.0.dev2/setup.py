import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

version_suffix = ''

try:
   with open('LOCAL-VERSION') as f:
      version_suffix = f.readline().strip()
except IOError:
   pass

setuptools.setup(
    name="ATPLibrary", # Replace with your own username
    version='0.1.0' + version_suffix,
    license="MIT",
    author="Wayne Vera",
    author_email="wayne.vera@expleogroup.com",
    description="Robotframework ATP Linrary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sqsglobal.visualstudio.com/ATP/_git/ATP.RobotFramework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['setupext-gitversion']
)