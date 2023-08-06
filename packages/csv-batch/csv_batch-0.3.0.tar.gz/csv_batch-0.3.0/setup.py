from setuptools import setup, find_packages


with open('requirements/requirements-test.txt') as f:
    test_requirements = f.read().splitlines()


setup(
    name='csv_batch',
    author='Mitchell Lisle',
    author_email='m.lisle90@gmail.com',
    description="A Python Encryption Helper Library",
    packages=find_packages(),
    setup_requires=[],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mitchelllisle/csv_batch',
    version='0.3.0',
    zip_safe=False,
)
