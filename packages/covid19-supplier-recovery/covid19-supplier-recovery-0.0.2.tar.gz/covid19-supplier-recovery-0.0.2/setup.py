from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
readme_path = path.join(this_directory, 'README.md')

with open(readme_path, encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='covid19-supplier-recovery',
    version='0.0.2',
    description='Modeling the recovery from covid19 crisis for suppliers to '
                'industries that have been severely impacted.',
    url='https://gitlab.com/DareData-open-source/covid-19-supplier-recovery',
    author='Ivo Bernardo, Sam Hopkins, Nuno Bras (DareData Engineering)',
    author_email='ivo@daredata.engineering',
    packages=['recoverymodel'],
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
