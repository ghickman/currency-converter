from setuptools import find_packages, setup


def long_desc():
    with open('README.rst') as f:
        return f.read()


setup(
    name='currency-converter',
    version='0.1.0',
    description='Currency converter',
    long_description=long_desc(),
    author='George Hickman',
    author_email='george@ghickman.co.uk',
    url='https://github.com/ghickman/currency-converter',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['click', 'requests'],
    entry_points={'console_scripts': [
        'currency-converter=currency_converter.main:cli',
    ]},
    classifiers=[
    ],
)
