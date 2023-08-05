import pathlib
from setuptools import setup

from dot import version as VERSION

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name='dotfile',
    version=VERSION,
    description='dot is an elegant git wrapper for managing dotfiles',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/kylepollina/dot',
    author='Kyle Pollina',
    author_email='kylepollina@pm.me',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['dot'],
    include_package_data=True,
    install_requires=['click', 'toml'],
    entry_points={
        'console_scripts': [
            'dot=dot.dot:main'
        ]
    },
)
