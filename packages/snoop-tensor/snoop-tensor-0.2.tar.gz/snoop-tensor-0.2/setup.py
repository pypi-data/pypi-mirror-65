from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='snoop-tensor',
    version="0.2",
    author='Jacob Zhong',
    author_email='cmpute@gmail.com',
    description="Tensor extension for snoop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cmpute/snoop-tensor',
    packages=find_packages(),
    install_requires=[
        'snoop',
    ],
    tests_require=[
        'pytest',
        'torch',
        'python-toolbox',
        'coverage',
        'snoop',
    ],
)
