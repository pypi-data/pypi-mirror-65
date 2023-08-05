'''
Created on Jan 18, 2019

@author: mboscolo
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FlaskTrytonWTF",
    version="0.0.3",
    author="Matteo Boscolo",
    author_email="matteo.boscolo@omniasolutions.eu",
    description="The project intend to or extendig the capabilities of flask in order to read and write data directely to tryton.",
    long_description=long_description,
    include_package_data=True,
    install_requires=['Flask-WTF', 'Flask-Table', 'flask-tryton'],
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/omniasolutions/flasktrytonwtf/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
