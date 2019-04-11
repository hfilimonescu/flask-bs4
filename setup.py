import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Flask-BS4',
    version='4.3.1.3',
    url='https://github.com/hfilimonescu/flask-bs4',
    license='MIT',
    author='Horia Filimonescu',
    author_email='horia.filimonescu+github@gmail.com',
    description='Include Bootstrap4 in your Flask project',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=['flask_bs4'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
        'dominate',
        'visitor',
    ],
    classifiers=[
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
