from setuptools import setup, find_packages

# with open('README.md') as readme_file:
#     README = readme_file.read()
#
# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='MachineHelper',
    version='0.0.3',
    description='Useful tools to work with Machine Learning in python',
    long_description_content_type="text/markdown",
    long_description="",
    license='MIT',
    packages=find_packages(),
    author='Vitor Sasaki Venzel',
    author_email='vitorsakivenzelv@gmail.com',
    keywords=['Sklearn', 'Machine Learning', 'Pandas'],
    url='https://github.com/vSasakiv/MachineHelper',
    download_url='https://pypi.org/project/MachineHelper2/',
    include_package_data=True
)

install_requires = [
    'sklearn',
    'numpy',
    'pandas',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)