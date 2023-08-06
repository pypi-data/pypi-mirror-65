from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='floydpink.jsii_native_python',
    version='0.0.1',
    description='A simple Python library to benchmark against a jsii module with similar, simple logic.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Hari Pachuveetil',
    author_email='imbleedingme@googlemail.com',
    keywords=['jsii', 'python', 'java', 'dotnet', 'typescript', 'aws'],
    url='https://github.com/floydpink/jsii-native-python',
    download_url='https://pypi.org/project/jsii-native-python/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)

