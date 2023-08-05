import re

from setuptools import setup


with open('README.rst', 'rt', encoding='utf8') as readme_file:
    README = readme_file.read()
with open('cornerstone/__init__.py', 'rt', encoding='utf8') as cornerstone_file:
    VERSION = re.search(r'__version__ = \'(.*?)\'', cornerstone_file.read()).group(1)


setup(
    name='CornerstoneCMS',
    version=VERSION,
    author='Raoul Snyman',
    description='A simple content management system for churches',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://cornerstonecms.org',
    project_urls={
        # 'Documentation': 'https://cornerstonecms.gitlab.io/',
        'Code': 'https://gitlab.com/cornerstonecms/cornerstonecms',
        'Issue tracker': 'https://gitlab.com/cornerstonecms/cornerstonecms/issues'
    },
    license='GPLv3+',
    packages=['cornerstone'],
    include_package_data=True,
    platforms='any',
    python_requires='>=3.5',
    install_requires=[
        'Flask',
        'Flask-Admin',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-User',
        'Flask-Themes2',
        'serpent',
        'pyyaml',
        'unidecode',
        'werkzeug==0.16.1'
    ],
    extras_require={
        'dev': [
            'pytest>=3',
            'pytest-cov',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
)
