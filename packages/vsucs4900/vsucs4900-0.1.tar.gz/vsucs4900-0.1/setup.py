from setuptools import setup
 
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
 
setup(
    name='vsucs4900',
    version='0.1',
    description='Demo for building a Python project',
    author='Lin Chen',
    author_email='lichen@valdosta.edu',
    url='http://lin-chen-va.github.io',
    install_requires=requirements,
    packages=['primepackage', ],
    package_dir={'':'src'},
    scripts=['src/generator',],
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
