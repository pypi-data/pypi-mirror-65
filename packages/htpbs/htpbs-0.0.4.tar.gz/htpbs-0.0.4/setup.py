from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='htpbs',
    version='0.0.4',
    description='A Python module that creates horizontal progress bars to keep track of the progress of threaded '
                'jobs. Progress Bars in this module are totally customizable',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Jose Ortiz',
    author_email='csjortizco@gmail.com',
    keywords=['Bars', 'Horizontal', 'Progress Bars', 'Threaded'],
    url='https://github.com/jortizcostadev/htpbs',
    download_url='https://pypi.org/project/htpbs/',
    python_requires='>=3.6'
)


install_requires = [

]


if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)