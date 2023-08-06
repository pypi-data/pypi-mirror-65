# This file is part of filestore-gs. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import os
import io
from setuptools import setup


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


setup(name='tryton-twilio',
    version='0.1.0',
    author='B2CK',
    author_email='info@b2ck.com',
    description='Send SMS from Tryton via Twilio',
    url='https://hg.b2ck.com/tryton-twilio',
    long_description=read('README'),
    py_modules=['tryton_twilio'],
    platforms='Posix; MacOS X; Windows',
    keywords='tryton twilio SMS',
    classifiers=[
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        ],
    license='GPL-3',
    install_requires=[
        'twilio',
        'trytond > 5.0',
        ])
