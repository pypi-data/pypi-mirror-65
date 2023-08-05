from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='onnconformity',
    version='0.0.2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://onnconformity.oznetnerd.com',
    install_requires=[],
    license='',
    author='Will Robinson',
    author_email='will@oznetnerd.com',
    description='Convenience Python module for Cloud One Conformity'
)
