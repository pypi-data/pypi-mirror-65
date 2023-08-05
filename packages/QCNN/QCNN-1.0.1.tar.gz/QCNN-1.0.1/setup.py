from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name = "QCNN",version="1.0.1",description="Deep Neural Network module for classification/regression",py_modules=['QCNN'],package_dir = {'':'src'},classifiers = [
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License'],
    long_description = long_description,
    long_description_content_type='text/markdown',
    install_requires = ['matplotlib~=2.2.2',
    'pandas~=0.22.0',
    'numpy~=1.18.2']


)
