import setuptools

setuptools.setup(
    name='pytest-modifyscope',
    version='0.1.1',
    author='Shungiku',
    author_email='shungiku@x06.org',
    description='pytest plugin to modify fixture scope',
    url='https://github.com/shungiku/pytest-modifyscope',
    packages=['pytest_modifyscope'],
    install_requires=['pytest'],
    entry_points={
        'pytest11': [
            'pytest_modifyscope = pytest_modifyscope',
        ],
    }
)