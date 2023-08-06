import os
import setuptools

project_folder = 'D:/python/projecten/pypeflow'
requirements_path = project_folder + '/requirements.txt'
install_requires = []

if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='tc_pypeflow',
    version='2020.0',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    url='',
    license='MIT License',
    author='Tom Christiaens',
    author_email='tom.chr@proximus.be',
    description='piping network design and analysis',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
