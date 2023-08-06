from distutils.core import setup
setup(
  name = 'MyAL',        
  packages = ['MyAL'],  
  version = '0.2',      
  license='MIT',        
  description = 'Get Data from My Anime List',   
  author = 'Sanjeev Kumar Bharadwaj (Nyzex)',               
  author_email = 'kamtinsithlou025@gmail.com',      
  url = 'https://github.com/Quanta-of-solitude/MyAL',   
  download_url = 'https://github.com/Quanta-of-solitude/MyAL/archive/0.2.tar.gz',    
  keywords = ['animelist', 'My Anime List', 'malgithub','MAL','MyAnimeList', 'MAL API'],   
  install_requires=[            # I get to this in a second
          'requests',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)