import ast
import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_treeify.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='Michael Vartanyan',
    author_email='mv@spherical.pm',
    description=description,
    keywords='Lektor plugin tree menu',
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-treeify',
    packages=find_packages(),
    py_modules=['lektor_treeify'],
    version='1.0',
    install_requires=[
        'more_itertools',
        'simplejson',
    ],
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
    ],
    entry_points={
        'lektor.plugins': [
            'treeify = lektor_treeify:TreeifyPlugin',
        ]
    }
)
