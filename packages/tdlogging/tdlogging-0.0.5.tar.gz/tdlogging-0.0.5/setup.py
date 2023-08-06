from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    README = readme_file.read()

with open('HISTORY.md', encoding='utf-8') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='tdlogging',
    version='0.0.5',
    description='Classed based logger for Python',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Terry Qi',
    author_email='troppydash.developer@gmail.com',
    keywords=['Logger', 'Class'],
    url='https://github.com/troppydash/tdlogging',
    download_url='https://pypi.org/project/tdlogging/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
