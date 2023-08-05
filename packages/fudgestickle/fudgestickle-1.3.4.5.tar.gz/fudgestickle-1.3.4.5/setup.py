from setuptools import setup

def readme():
    with open('README.md', 'r') as f:
        README = f.read()
    return README

setup(
    name='fudgestickle',
    version='1.3.4.5',
    description='a package for auto generating the code for an updated "this means war" game\'s score table',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/cugzarui/fudgestickle',
    author='revolution and cugz',
    author_email='Roey.eshkar@gmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages=['fudgestickle'],
    include_package_data=False,
    install_requires=['htmldom'],
    entry_points = {
        "console_scripts": [
            "fudgestickle=fudgestickle.cli:main",
        ]
    },
)