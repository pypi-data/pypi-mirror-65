# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'shub-workflow',
    version      = '1.6.5',
    description  = 'Workflow manager for scrapinghub ScrapyCloud tasks.',
    long_description = open('README.md').read(),
    license      = 'BSD',
    url          = 'https://github.com/scrapinghub/shub-workflow',
    maintainer   ='Scrapinghub',
    packages     = find_packages(),
    install_requires = (
        'pyyaml>=3.12',
        'retrying>=1.3.3',
        'scrapinghub>=2.0.3',
        'jinja2>=2.7.3',
        'sqlitedict==1.6.0',
        's3fs==0.2.0',
        'boto3>=1.9.92',
        'msgpack-python',
    ),
    scripts = [],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
