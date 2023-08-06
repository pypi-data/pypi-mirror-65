# -*- coding: utf-8 -*- 
"""
@User     : Frank
@File     : setup.py
@DateTime : 2019-09-16 11:24 
@Email    : 15769162764@163.com
"""
from setuptools import setup, find_packages
import io
import re

with io.open('README.rst', 'r', encoding='utf8') as f:
    long_description = f.read()

with io.open("src/useful_decoration/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="useful_decoration",
    license='Apache License 2.0',
    version=version,
    packages=find_packages("src"),
    zip_safe=False,
    include_package_data=True,
    package_dir={"": "src"},
    long_description=long_description,
    url='https://github.com/changyubiao/useful_decoration',
    author='frank',
    author_email='15769162764@163.com',
    description='powerful and useful decorations',

    project_urls={
        "Documentation": "https://useful-decoration.readthedocs.io/en/latest/",
        "Code": "https://github.com/changyubiao/useful_decoration",
    },

    python_requires='>=3.6',
    install_requires=[
        "pysimple-log",

    ],

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

)
