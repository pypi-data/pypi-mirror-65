import sys
import setuptools
from setuptools.dist import Distribution

videocapture_download_url = 'https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/VideoCapture-0.9.5-%s.whl'

def wheel_distname_name_tag(**kwargs):
    # create a fake distribution from arguments
    dist = Distribution(attrs=kwargs)
    # finalize bdist_wheel command
    bdist_wheel_cmd = dist.get_command_obj('bdist_wheel')
    bdist_wheel_cmd.ensure_finalized()
    # assemble wheel file name
    distname = bdist_wheel_cmd.wheel_dist_name
    tag = bdist_wheel_cmd.get_tag()
    return '%s-%s.whl' % (distname, '-'.join(tag)), distname, tag

options = dict(
    name = 'SeeMee',
    version = '0.0.3',
    url = 'https://github.com/gaming32/SeeMee',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = "Detects which camera you're looking at",
    long_description = '',
    long_description_content_type = 'text/markdown',
    dependency_links = [],
    install_requires = [
        'tensorflow',
        'pygame',
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
    },
    zip_safe = False,
)

if sys.platform[:3] == 'win':
    videocapture_download_url = videocapture_download_url % '-'.join(wheel_distname_name_tag(**options)[2])
    options['dependency_links'].append(videocapture_download_url)

# print(videocapture_download_url)

setuptools.setup(**options)