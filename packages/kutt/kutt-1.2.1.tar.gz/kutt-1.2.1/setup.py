from setuptools import setup

setup(
    name='kutt',
    version='1.2.1',
    author='Amirali Esfandiari',
    author_email='amiralinull@gmail.com',
    url='http://github.com/realamirali/kutt-cli',
    py_modules=['kutt'],
    install_requires=['fire', 'requests'],
    packages=['kutt'],
    package_dir={'kutt': 'kutt'},
    python_requires='>=3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ],
    entry_points = '''
        [console_scripts]
        kutt=kutt.cli:main
    ''',
)
