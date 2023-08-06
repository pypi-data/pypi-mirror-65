import setuptools
import ssd1362

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    

setuptools.setup(
    name="ssd1362-py",
    version=ssd1362.__version__,

    author="mrzjo",
    author_email="mrzjo05@gmail.com",
    url="https://gitlab.com/telelian/peripheral-library/ssd1362.git",

    description="ssd1362 for python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    packages=setuptools.find_packages(),

    install_requires=[
        'numpy>=1.18.1'
        ,'spidev>=3.4'
        ,'g4l>=0.1.2'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware'
    ],
)
