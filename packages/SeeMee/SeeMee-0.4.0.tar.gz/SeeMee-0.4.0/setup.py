import sys
import setuptools

options = dict(
    name = 'SeeMee',
    version = '0.4.0',
    url = 'https://github.com/gaming32/SeeMee',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = "Detects which camera you're looking at",
    long_description = '',
    long_description_content_type = 'text/markdown',
    install_requires = [
        'tensorflow',
        'pygame',
    ],
    data_files = [],
    python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    packages = [
        'SeeMee',
    ],
    ext_modules = [
        setuptools.Extension('SeeMee.base', ['SeeMee/base.c']),
    ],
    entry_points = {
        'gui_scripts': [
            'seemee = SeeMee.base:main',
        ],
    },
    zip_safe = False,
)

if sys.platform[:3] == 'win':
    options['install_requires'].append('VideoCapture')

setuptools.setup(**options)