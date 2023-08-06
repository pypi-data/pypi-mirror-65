from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='fortmatic',
    version='0.0.7',
    description='Fortmatic Python Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fortmatic',
    author_email='support@fortmatic.com',
    url='https://fortmatic.com',
    license='MIT',
    keywords='fortmatic python sdk',
    packages=find_packages(
        exclude=[
            'tests',
            'tests.*',
            'examples',
            'examples.*',
            'testing',
            'testing.*',
        ],
    ),
    zip_safe=False,
    install_requires=[
        'requests == 2.22',
        'web3 == 5.4.0',
        'retrying == 1.3.3',
    ],
    python_requires='>=3.6',
    project_urls={
        'Website': 'https://fortmatic.com',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
