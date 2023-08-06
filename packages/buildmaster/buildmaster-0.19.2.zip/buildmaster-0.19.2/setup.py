# Always prefer setuptools over distutils
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

install_requires = [
    "SQLAlchemy>=1.3.11",
    "PyMySQL>=0.9.3",
    "Flask>=1.0.2",
    "Flask-Cors>=3.0.4",
    "tornado>=6.0.2",
    "flask_restplus>=0.12.1",
    "Flask-JWT-Extended>=3.18.1",
    "captcha>=0.3",
    "Wand>=0.5.9",
    "Werkzeug==0.16.1",
    "pandas>=0.24.2",
    "psutil>=5.7.0",
    "openpyxl>=3.0.0",
]
setup(
    name='buildmaster',
    version='0.19.2',
    description='web-based management system builder',

    # The project's main homepage.
    url='https://gitee.com/rushmore/buildmaster',

    # Author details
    author='Rushmore (Leiming Hong)',
    author_email='hong.leiming@qq.com',

    # Choose your license
    license='LGPL',

    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
    ],
    include_package_data=True,
    install_requires=install_requires,
    keywords='DB',
    packages=find_packages()
)
