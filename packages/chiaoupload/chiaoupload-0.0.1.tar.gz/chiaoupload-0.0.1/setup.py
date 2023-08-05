from setuptools import setup, find_packages
from os import path
from io import open
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chiaoupload',  # Required
    version='0.0.1',  # Required
    description='test upload package',  # Optional
    #long_description=long_description,  # Optional
    #long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/luckchiao',  # Optional
    author='chiao',  # Optional
    author_email='luckchiao@gmail.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='python',  # Optional
    packages=find_packages(exclude=['pandas']),
)
