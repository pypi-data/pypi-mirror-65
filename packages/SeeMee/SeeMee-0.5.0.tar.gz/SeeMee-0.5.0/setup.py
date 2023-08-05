import setuptools

setuptools.setup(
    name = 'SeeMee',
    version = '0.5.0',
    url = 'https://github.com/gaming32/SeeMee',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = "Application which detects which camera you're looking at",
    long_description = '',
    long_description_content_type = 'text/markdown',
    install_requires = [
        'tensorflow',
        'pygame',
        'VideoCapture; platform_system=="Windows"'
    ],
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
        'console_scripts': [
            'seemee_con = SeeMee.base:main',
        ],
    },
    zip_safe = False,
)