from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='dataset2database',
    version='0.0.1',
    description='Useful converter of videos to SQL databases for Python',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='GPL-3.0',
    packages=find_packages(),
    author='Alexandros Stergiou',
    author_email='alexstergiou5@gmail.com',
    keywords=['SQLconverter', 'dataset2database', 'JPG2SQL'],
    url='https://github.com/alexandrosstergiou/dataset2database',
    download_url='https://pypi.org/project/dataset2database/'
)

install_requires = [
    'opencv-python>=4.2.0.32',
    'numpy>=1.18.1'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
