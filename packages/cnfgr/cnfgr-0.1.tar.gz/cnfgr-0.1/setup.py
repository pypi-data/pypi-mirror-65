from distutils.core import setup
setup(
  name = 'cnfgr',         # How you named your package folder (MyLib)
  packages = ['cnfgr'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Configuration management base on python files only.',   # Give a short description about your library
  author = 'Divesh Naidu',                   # Type in your name
  author_email = 'diveshnaidu18@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Rfrixy/cnfgr',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Rfrixy/cnfgr/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['configuration', 'conf', 'keys'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)