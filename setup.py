from setuptools import setup, find_packages

setup(
    name='nous.pystat',
    version='0.1',
    description='Utilities to collect interesting stats about your code.',
    author='Ignas Mikalajunas',
    author_email='ignas@nous.lt',
    url='http://github.com/Ignas/nous.pystat/',
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 "Programming Language :: Python"],
    install_requires=[
        'decorator',
#        'py-itimer' # XXX make it an "extra" dependency, can't recall how now
        ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    license="GPL"
)
