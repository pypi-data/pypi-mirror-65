from setuptools import setup, find_packages


__version__ = '0.1.0'


develop_requires = [
    'autopep8',
    'flake8',
    'pep8-naming',
]


try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''


setup(
    name='pyautocast',
    version=__version__,
    author='ctgk',
    author_email='r1135nj54w@gmail.com',
    maintainer='ctgk',
    maintainer_email='r1135nj54w@gmail.com',
    url='https://github.com/ctgk/pyautocast',
    description='Automatic function arguments casting',
    long_description=readme,
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],

    packages=find_packages(exclude=('test*',)),
    python_requires=">=3.7",
    extras_require={"develop": develop_requires},

    test_suite="tests",
)
