from setuptools import setup, find_packages
setup(
  name = 'ftg',
  packages = find_packages(),
  version = '0.7',
  license='MIT',
  description = 'A generator for a flask app template',
  author = 'Nicholas Ong Wei Harn',                
  author_email = 'nicholasowh@hotmail.com',   
  url = 'https://github.com/qaqaqaqaowh/ftg',
  download_url = 'https://github.com/qaqaqaqaowh/ftg/archive/0.7.tar.gz', 
  keywords = ['flask', 'template', 'generate'],
  install_requires=[         
          'flask',
          'peewee',
          'peewee-db-evolve',
          'python-dotenv',
          'psycopg2-binary',
          'Flask-Assets',
          'cssmin',
          'jsmin',
          'Flask-Cors'
      ],
  entry_points = {
    'console_scripts': ['ftg=src.__main__:main'],
  },
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7'
  ],
)