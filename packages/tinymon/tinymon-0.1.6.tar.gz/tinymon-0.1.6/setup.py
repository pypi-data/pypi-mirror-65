from setuptools import setup, Extension, find_packages
import tinymon

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    

setup(
    name="tinymon",
    version=tinymon.__version__,

    author="mrzjo",
    author_email="mrzjo05@gmail.com",
    url="https://gitlab.com/telelian/peripheral-library/tinymon",

    description="tinymon",
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    packages=find_packages(),
    
    package_data = {
        'tinymon': ['font/*', 'image/videonot.png'],
    },
    zip_safe=False,

    install_requires=[
        'numpy>=1.18.1'
        ,'Pillow>=7.0.0'
        ,'ssd1362-py>=0.1.1'
        ,'loguru>=0.4.1'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware'
    ],
)
