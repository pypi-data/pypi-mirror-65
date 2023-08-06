from setuptools import setup

with open('README.rst', 'r') as file_object:
    readme = file_object.read()

setup(
    name = 'envassume',
    version = '1.0.7',
    description = 'Assume an AWS IAM role and execute a command with the assumed credentials',
    long_description = readme,
    license = 'MIT',
    author = 'Warren Moore',
    author_email = 'warren@wamonite.com',
    url = 'https://github.com/wamonite/envassume',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    packages = ['envassume'],
    entry_points = dict(console_scripts = ['envassume=envassume.main:run']),
    install_requires = [
        'boto3',
        'attrs',
    ],
    zip_safe = False,
)
