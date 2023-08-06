from setuptools import setup
setup(name='pythonspell',
    version='0.61',
    description='A simple python spellchecker built on BK Trees and Damerau Levenshtein distance',
    url='https://github.com/AidanJSmith',
    long_description = "file:README.rst",
    author='Aidan Smith',
    author_email='100023755@mvla.net',
    license='MIT',
    keywords='spelling corrector autocorrect',
    packages=['pyspell'],
    zip_safe=False)