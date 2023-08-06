

from distutils.core import setup

setup(
  name = 'coronaupdates',         # How you named your package folder (MyLib)
  packages = ['coronaupdates'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Command Line Interface for retrieving CoViD-19 related informations.',   # Give a short description about your library
  author = 'Arjun Adhikari',                   # Type in your name
  author_email = 'mailarjunadhikari@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/thearjun/coronaupdates',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/theArjun/coronaupdates/archive/v1.0.tar.gz',    # I explain this later on
  keywords = ['covid', 'coronaupdates', 'corona', 'virus', 'pandemic'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'lxml',
          'requests',
          'tabulate',
          'bs4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)