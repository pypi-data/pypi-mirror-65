from distutils.core import setup
setup(
  name = 'dbsession',
  packages = ['dbsession'],  
  version = '0.5.3',      
  license='MIT',       
  description = 'The python postgreSQL ORM ',  
  author = 'imwiwiim90',                   
  author_email = 'imwiwiim90@gmail.com',      
  url = 'https://github.com/imwiwiim90/dbsession',   
  download_url = 'https://github.com/imwiwiim90/dbsession/archive/v_05.tar.gz',    # I explain this later on
  keywords = ['python', 'postgreSQL', 'ORM', 'psycopg2'],   
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',     
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)