from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

required = [
    'requests',
]

extras = {
    'develop': [
        'mypy==0.770',
        'pylint==2.4.4',
        'setuptools==46.1.3',
        'twine==3.1.1',
    ]
}

setup(
    name='pp_up',
    version='0.0.0rc1',
    author='Johan B.W. de Vries',
    description='Update pypi dependencies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jbwdevries/pp-up',
    project_urls={
        'Bug Tracker': 'https://github.com/jbwdevries/pp-up/issues',
        'Source Code': 'https://github.com/jbwdevries/pp-up',
    },
    packages=['pp_up'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    setup_requires=[
        'wheel',
    ],
    install_requires=required,
    extras_require=extras,
)
