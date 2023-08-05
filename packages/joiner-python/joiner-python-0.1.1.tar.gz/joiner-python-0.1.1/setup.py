import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

setup(
    name='joiner-python',
    version=__import__('joiner').__version__,
    description='a tiny library for merging groups of data in a sql-join-like way',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='ZouYJ',
    author_email='boyzouyj@gmail.com',
    url='https://github.com/boy-zyj/joiner-python.git',
    py_modules=['joiner'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT License',
    platforms=['any'],
    zip_safe=False)
