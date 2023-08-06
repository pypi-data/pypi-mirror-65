"""
Flask-Profiler
-------------

Flask Profiler

Links
`````

* `development version <http://github.com/saivarunr/flask-profiler/>`

"""
import sys
from setuptools import setup


tests_require = [
    "Flask-Testing",
    "simplejson",
    "sqlalchemy"
]

install_requires = [
    'Flask',
    'Flask-HTTPAuth',
    'simplejson'
]

setup(
    name='flask_profiler_logger',
    version='1.0',
    url='https://github.com/saivarunr/flask-profiler',
    license=open('LICENSE').read(),
    author='Sai Varun Reddy Daram',
    author_email='saivarunvishal@gmail.com',
    description='API endpoint profiler for Flask framework',
    keywords=[
        'profiler', 'flask', 'performance', 'optimization'
    ],
    packages=['flask_profiler'],
    test_suite="tests.suite",
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
