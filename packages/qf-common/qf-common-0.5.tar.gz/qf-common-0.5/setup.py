from setuptools import setup


# python setup.py sdist bdist_wheel
# twine upload dist/* -u stefanovich

setup(
    name='qf-common',
    version='0.5',
    author='Anton Stefanovich',
    description='Useful things for QF projects',
    url='https://github.com/quality-first/qf-common',
    author_email='anton.stefanovich@gmail.com',
    packages=['qf_common'],
    zip_safe=False,
    license='MIT',
)
