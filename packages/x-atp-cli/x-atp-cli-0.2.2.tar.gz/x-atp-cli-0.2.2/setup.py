from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='x-atp-cli',
    version='0.2.2',
    keywords=['x', 'atp', 'test', 'platform'],
    description='X automated test platform command line client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    url='https://github.com/hekaiyou/x-atp-cli',
    author="HeKaiYou",
    author_email="hekaiyou@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'xlrd',
        'xlsxwriter',
        'pillow',
        'selenium',
        'injson',
        'requests-toolbelt',
        'requests',
        'redis',
    ],
    entry_points={
        'console_scripts': [
            'x-atp-cli = atp.cli:main'
        ]
    },
)
