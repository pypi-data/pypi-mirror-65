from io import open
from setuptools import find_packages, setup

with open('monoff/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'
with open('README.md','r') as f:
    readme = f.read()

REQUIRES = []

setup(
    name='monoff',
    version=version,
    description='Simple script to turn off all monitors',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Matthew Miguel',
    author_email='mmiguel6288code@gmail.com',
    maintainer='Matthew Miguel',
    maintainer_email='mmiguel6288code@gmail.com',
    url='https://github.com/mmiguel6288code/monoff',
    license='MIT',
    keywords=[
        'monitors','power','dpms','monitor','off','turn off','power down',
    ],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    install_requires=REQUIRES,
    tests_require=[],
    packages=find_packages(),
)
