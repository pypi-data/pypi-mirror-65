from setuptools import setup
 
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
 
setup(
    name='vsucs4900c', # a unique name for PyPI
    version='0.1',
    description='Demo for building a Python project',
    author='Lin Chen',
    author_email='lichen@valdosta.edu',
    url='https://github.com/lin-chen-GA/prime',
    install_requires=requirements,
    packages=['primepackage', ], # packages and subpackages containing .py files
    package_dir={'':'src'}, # location to find the packages
    scripts=['src/generator',], # the executable files will be installed for user
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
)
