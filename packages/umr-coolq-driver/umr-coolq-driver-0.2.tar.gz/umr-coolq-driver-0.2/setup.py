import sys
from setuptools import setup, find_packages

import pathlib
import re

WORK_DIR = pathlib.Path(__file__).parent

if sys.version_info < (3, 7):
    raise Exception("Python 3.7 or higher is required. Your version is %s." % sys.version)

long_description = open('README.md', encoding="utf-8").read()

def get_version():
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'umr_coolq_driver' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__VERSION__ = (.*)[\r\n]?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setup(
    name='umr-coolq-driver',
    packages=find_packages(include=['umr_coolq_driver', 'umr_coolq_driver.*']),
    version=get_version(),
    description='UMR Coolq Driver',
    long_description=long_description,
    author='Curtis Jiang',
    url='https://github.com/jqqqqqqqqqq/UnifiedMessageRelay',
    license='MIT',
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
    keywords=['UMR', 'UnifiedMessageRelay', 'Group chat relay', 'IM', 'messaging', 'QQ'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Typing :: Typed"
    ],
    install_requires=[
        'aiocqhttp',
        'unified-message-relay',
        'janus',
    ],
    project_urls={
        "Telegram Chat": "https://t.me/s/UnifiedMessageRelayDev",
    }
)
