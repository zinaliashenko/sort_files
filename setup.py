from setuptools import setup

setup(
    name='clean_folder',
    version='0.0.1',
    description='clean_folder is a Python package sorting files',
    url='https://github.com/zinaliashenko/clean_folder',
    author='Zinaida Liashenko',
    author_email='liashenkozina@gmail.com',
    license='MIT',
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)