'''
Created on 20200203
Update on 20200203
@author: Eduardo Pagotto
'''

from subprocess import check_call

import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

PACKAGE = "FlaskStreaming"
VERSION = __import__(PACKAGE).__version__

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        #check_call("apt-get install this-package".split())
        check_call("echo 'DevelopInstall'".split())
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        #check_call("apt-get install this-package".split())
        check_call("echo 'POSTINSTALL'".split())
        install.run(self)

setuptools.setup(
    include_package_data=True, # para adicionar o manifest
    name="FlaskStreaming",
    version=VERSION,
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="Video stream com flask",
    long_description="Video stream com flask",
    long_description_content_type="text/markdown",
    url="https://github.com/newspacebpo/FlaskStreaming.git",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    scripts=['app.py'],
    data_files=[('etc',['./etc/FlaskStream.yaml']),
                ('templates',['./templates/index.html'])],
    install_requires=['click',
                      'Flask',
                      'itsdangerous',
                      'Jinja2',
                      'MarkupSafe',
                      #'picamera',
                      'Werkzeug',
                      'python3-logstash'],
        cmdclass={'develop': PostDevelopCommand,
                  'install': PostInstallCommand,}
)
