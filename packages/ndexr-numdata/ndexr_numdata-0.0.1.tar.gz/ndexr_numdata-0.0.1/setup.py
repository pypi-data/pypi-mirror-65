from setuptools import setup, find_packages

with open('README.md', "r") as fh:
    long_description = fh.read()

setup(
    name='ndexr_numdata',
    version='0.0.1',
    author='Freddy Drennan',
    author_email='drennanfreddy@gmail.com',
    description='A simple package calculating values for a single number and created in my Udemy course',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/fdrennan/ndexr_numdata',
    keywords='package numbers calculations',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    # install_requires=['pandas'],
    python_requires='>=3.4'
)
