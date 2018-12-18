"""
nbreport
"""

import codecs
import os
from setuptools import setup, find_packages
import nbreport

install_requires = []

setup(
    name="nbreport",
    description="Generate quick reports",
    long_description='',
    version=nbreport.__version__,
    packages=find_packages(),
    package_data={'sphinx_gallery': ['static/report.tpl']},
    url="https://github.com/choldgraf/nbreport",
    author="Chris Holdgraf",
    author_email='choldgraf@berkeley.edu',
    install_requires=install_requires,
    license='3-clause BSD',
    classifiers=['Intended Audience :: Developers',
                 'Development Status :: 3 - Alpha',
                 'Framework :: Sphinx :: Extension',
                 'Programming Language :: Python',
                 ],
    entry_points={
        'console_scripts': [
            'nbreport = nbreport:main',
    ]},
    include_package_data=True,
    data_files=[
        ("nbreport/static/", ["nbreport/static/report.tpl", 'nbreport/static/extra.css']),
    ],
    zip_safe=False
)
