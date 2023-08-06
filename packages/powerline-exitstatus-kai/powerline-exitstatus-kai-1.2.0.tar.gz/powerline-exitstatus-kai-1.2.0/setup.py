# vim:fileencoding=utf-8:noet

from setuptools import setup

setup(
    name         = 'powerline-exitstatus-kai',
    description  = 'A Powerline segment for showing the status of Exit status',
    version      = '1.2.0',
    keywords     = ['powerline exit status prompt','powerline','shell','console'],
    license      = 'MIT',
    author       = 'i0ntempest',
    author_email = 'szf1234@me.com',
    url          = 'https://github.com/i0ntempest/powerline-exitstatus-kai',
    download_url = 'https://github.com/i0ntempest/powerline-exitstatus-kai/archive/v1.2.0.tar.gz',
    packages     = ['powerline_exitstatus_kai'],
    install_requires = ['powerline-status'],
    classifiers  = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals'
    ]
)