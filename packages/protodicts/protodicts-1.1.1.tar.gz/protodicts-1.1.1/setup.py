from setuptools import setup


setup(
    name='protodicts',
    description='a small Python library for 2 ways conversion between dicts '
                'and protocol buffers.',
    version='1.1.1',
    author='Eugene Van den Bulke',
    author_email='eugene.vandenbulke@gmail.com',
    url='https://github.com/alexyvassili/protodicts',
    license='Public Domain',
    keywords=['protobuf', 'dict'],
    install_requires=['protobuf>=2.3.0', 'six'],
    package_dir={'': 'src'},
    py_modules=['protodicts'],
    # setup_requires=['protobuf>=2.3.0', 'nose>=1.0', 'coverage', 'nosexcover'],
    # test_suite = 'nose.collector',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
