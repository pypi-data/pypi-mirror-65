from distutils.core import setup

setup(
  name = 'proc_plot',
  packages = ['proc_plot'],
  version = '0.1',
  license='GPLv3', 
  description = 'Trending for Process Control Data Analysis',
  author = 'Francois Pieterse',
  author_email = 'francois.pieterse@greenferndynamics.com',
  url = 'https://github.com/fpieterse/proc_plot',
  download_url = 'https://github.com/fpieterse/proc_plot/archive/v0.1.tar.gz',
  keywords = ['Trend','Process Control'],
  install_requires=[
          'pandas',
          'matplotlib',
          'PyQt5',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Manufacturing',      # Define that your audience are developers
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
