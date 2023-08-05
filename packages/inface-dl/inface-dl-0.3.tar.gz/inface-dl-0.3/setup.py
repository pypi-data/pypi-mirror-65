from distutils.core import setup
setup(
  name = 'inface-dl',         # How you named your package folder (MyLib)
  packages = ['inface-dl'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = '''Video Downloader

Example Code:

>>> # instagram video downloader
>>> import inface-dl
>>> ses = inface-dl.Session()
>>> ses.ig(url='url here', output='output.mp4')


>>> # facebook video downloader
>>> import inface-dl
>>> ses = inface-dl.Session()
>>> ses.fb(url='url here', output='output.mp4')''',   # Give a short description about your library
  author = 'sCuby07',                   # Type in your name
  author_email = 'ajaanonk@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/anonkyuhuu/inface-dl',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/inface-dl.tar.gz',    # I explain this later on
  keywords = ['download', 'python', 'video'],   # Keywords that define your package best
  install_requires=['requests', 'bs4', 're'],
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
