import os
import unithandler
from setuptools import setup, find_packages

NAME = 'unithandler'
AUTHOR = 'Lars Yunker'

PACKAGES = find_packages()
KEYWORDS = ', '.join([
    'units',
    'unit',
    'float',
    'int'
])

readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
try:
    from m2r import parse_from_file
    readme = parse_from_file(readme_file)
except (ImportError, ModuleNotFoundError):
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        readme = f.read()

setup(
    name=NAME,
    version=unithandler.__version__,
    description='numeric mimic classes with units',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author=AUTHOR,
    url='https://gitlab.com/larsyunker/unithandler',
    packages=PACKAGES,
    license='MIT License',
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Operating System :: OS Independent',
        'Natural Language :: English'
    ],
    keywords=KEYWORDS,
    install_requires=[
        # 'numpy',
    ],
    project_urls={
        'Documentation': 'https://unithandler.readthedocs.io/en/latest/index.html'
    },
)
