import setuptools
import os
version = os.environ.get('VERSION', 3)
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gw-md-lib',
    version='0.10.{}'.format(version),
    author="Auriz",
    author_email="edominguez@auriz.biz",
    description="Common lib to GW project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=["Flask", "Flask-SQLAlchemy==2.4.0", "Flask-JWT-Extended==3.21.0"],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
