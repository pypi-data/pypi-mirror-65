import kuob
import sys
from setuptools import setup

if sys.version_info.major < 3:
    sys.exit('Python < 3 is unsupported.')

requirements = []
test_requirements = ['nose']

with open('README.md', encoding='utf8') as file:
    long_description = file.read()

setup(
    name='kuob',
    version='1.0.1',
    packages=['kuob', 'kuob.commands', 'kuob.asciicast'],
    license='GNU GPLv3',
    description='a Fork of ASCIINEMA Terminal session recorder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mohatb',
    author_email='mohatb@gmail.com',
    url='https://kuob.sh',
    entry_points={
        'console_scripts': [
            'kuob = kuob.__main__:main',
        ],
    },
    package_data={'kuob': ['data/*.png']},
    data_files=[('share/doc/kuob', ['CHANGELOG.md',
                                         'CODE_OF_CONDUCT.md',
                                         'README.md',
                                         'doc/asciicast-v1.md',
                                         'doc/asciicast-v2.md']),
                ('share/man/man1', ['man/kuob.1'])],
    install_requires=requirements,
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
)
