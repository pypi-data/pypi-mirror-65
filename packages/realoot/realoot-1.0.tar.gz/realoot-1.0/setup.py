"""


"""
from setuptools import find_packages
from setuptools.dist import Distribution
from distutils.core import setup, Extension
import pathlib
import os

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "realoot/README.md").read_text()

class BinaryDistribution(Distribution):

  def has_ext_modules(self):
    return True


EXTENSION_LIBS = []
if os.name == 'nt':
    EXTENSION_LIBS = ['_main.pyd', '_constants.pyd']
else:
    EXTENSION_LIBS = ['_main.so', '_constants.so']

setup(	name = "realoot", 
		version = '1.0',
		author = 'Joris T. OLYMPIO',
        author_email = 'jto.devs@gmail.com',
		description = """Solve the averaged low-thrust optimal control transfer problem""",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://gitlab.com/jorispio/realoot",
        license="GPLv3",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering',            
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        keywords='"optimal control" "space trajectory" orbit', 
        python_requires='>=3.7',
        packages=find_packages(),
        include_package_data=True,
        package_data={'main': EXTENSION_LIBS, 'examples': ['ex2.xml']},        
        install_requires=[],
        distclass=BinaryDistribution,
)
