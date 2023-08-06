from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

description = "Python package implements design patterns in generic way. Its can be used in a wide range of projects."

setup(
    name='generic_design_patterns',
    version='1.0.7',
    packages=['generic_design_patterns'],
    url='https://github.com/ShadowCodeCz/generic_design_patterns',
    project_urls={
        'Source': 'https://github.com/ShadowCodeCz/generic_design_patterns',
        'Tracker': 'https://github.com/ShadowCodeCz/generic_design_patterns/issues',
    },
    author='ShadowCodeCz',
    author_email='shadow.code.cz@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    keywords='design patterns event chain specification',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    install_requires=['yapsy']
)
