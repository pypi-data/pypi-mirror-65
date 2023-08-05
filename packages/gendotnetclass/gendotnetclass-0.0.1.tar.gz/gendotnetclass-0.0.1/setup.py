from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='gendotnetclass',
    version='0.0.1',
    description='Generate code for dotnet',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Louis Chen',
    author_email='scu.louis@gmail.com',
    keywords=['GenDotNetCode', 'GenDotNetCodeSearch', 'GenDotNetCodeStack'],
    url='https://github.com/sculouis/GenDotnetClass',
    download_url='https://pypi.org/project/gendotnetclass/'
)

install_requires = [
    'openpyxl>=2.6.2'
    'pytest==5.4.0'
    'mako==1.1.2'
    'dependency-injector==3.15.6'
    'PyYAML==5.3.1'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)