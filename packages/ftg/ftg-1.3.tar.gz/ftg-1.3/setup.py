from setuptools import setup, find_packages
setup(
  name = 'ftg',
  packages = find_packages(),
  version = '1.3',
  license='MIT',
  description = 'A generator for a flask app template',
  author = 'Nicholas Ong Wei Harn',                
  author_email = 'nicholasowh@hotmail.com',   
  url = 'https://github.com/qaqaqaqaowh/ftg',
  download_url = 'https://github.com/qaqaqaqaowh/ftg/archive/1.3.tar.gz', 
  keywords = ['flask', 'template', 'generate'],
  include_package_data = True,
  entry_points = {
    'console_scripts': ['ftg=src.__main__:main'],
  },
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)