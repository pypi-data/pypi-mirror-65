from importlib.machinery import SourceFileLoader

from setuptools import setup

# avoid loading the package before requirements are installed:
version = SourceFileLoader('version', 'zo/version.py').load_module()
setup(
    name='zo',
    version=str(version.VERSION),
    description='zo',
    long_description='zo',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author='zo',
    author_email='zo@dai3.com',
    url='https://github.com/daiooo/zo',
    license='',
    packages=['zo'],
    python_requires='>=3.7',
    zip_safe=False,
    install_requires=[
        'pydantic'
    ],
)
