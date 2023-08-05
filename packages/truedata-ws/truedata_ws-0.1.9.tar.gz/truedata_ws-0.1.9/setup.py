from setuptools import setup
# from .truedata_ws import version


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='truedata_ws',
    version='0.1.9',
    packages=['truedata_ws', 'truedata_ws.websocket'],
    url='',
    license='',
    author='Paritosh Chandran',
    author_email='paritosh.j.chandran@gmail.com',
    description="Truedata's Official Python Package",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
