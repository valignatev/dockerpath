from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='dockerpath',
    version='0.0.1a',
    description='Import python modules straight from docker containers!',
    long_description=readme,
    author='Valentin Ignatyev',
    author_email='valentjedi@gmail.com',
    url='https://github.com/valentjedi/dockerpath',
    license=license,
    packages=['dockerpath'],
    install_requires=['docker>=2.5'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

)
