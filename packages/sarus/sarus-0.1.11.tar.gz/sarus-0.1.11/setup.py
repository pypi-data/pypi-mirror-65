from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(

  name = 'sarus',         # How you named your package folder (MyLib)
  packages = ['sarus'],   # Chose the same as "name"
  version = '0.1.11',      # Start with a small number and increase it with every change you make
  license='Apache License 2.0',       # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python client for the Sarus Gateway.',
  long_description=long_description,
  author = 'Sarus Technologies',                   # Type in your name
  author_email = 'contact@sarus.tech',      # Type in your E-Mail
 # url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
 # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['differential privacy', 'AI', 'Data privacy'],   # Keywords that define your package best
  install_requires=[            
          'cloudpickle >=1.2',
           'tensorflow >=2.0',
           'numpy >=1.17',
           'matplotlib >=3.1',
           'tensorflow-io >=0.11'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
