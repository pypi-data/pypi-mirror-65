from setuptools import setup
with open('README.rst') as f:
    long_description = f.read()
setup(name='pythonspell',
    version='1.00',
    description='A simple python spellchecker built on BK Trees and Damerau Levenshtein distance',
    url='https://github.com/AidanJSmith',
    long_description = long_description,
    author='Aidan Smith',
    author_email='100023755@mvla.net',
    license='MIT',
    keywords='spelling corrector autocorrect',
    packages=['pyspell'],
    zip_safe=False)