# -*- coding: utf-8 -*-
'''
Created on 2018. 9. 19.
@author: Hyechurn Jang, <hyjang@cisco.com>
'''

import os
from setuptools import setup

def read(fname): return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name='vvv_vra',
    version='0.1.3',
    license='Apache 2.0',
    author='Hyechurn Jang',
    author_email='jangh@vmware.com',
    url='https://github.com/HyechurnJang/vvv_vra',
    description='VMware vRealize Automation Python SDK (based event driven<gevent>)',
    long_description=read('README'),
    long_description_content_type="text/markdown",
    packages=['vvv_vra', 'vvv_vra.schema', 'vvv_vra.schema.iaas'],
    install_requires=['pygics'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
    ],
)

# python setup.py sdist bdist_wheel
# twine upload dist/*