from distutils.core import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
  name = 'kydavra',
  packages = ['kydavra'],
  version = '0.1.1',
  license='MIT',
  description = 'Kydavra is a sci-kit learn inspired python library with feature selection methods for Data Science and Macine Learning Model development',
  long_description=long_description,
  author = 'SigmoidAI - Păpăluță Vasile',
  author_email = 'vpapaluta06@gmail.com',
  url = 'https://github.com/user/reponame',
  download_url = 'https://github.com/ScienceKot/kydavra/archive/v1.0.tar.gz',    # I explain this later on
  keywords = ['ml', 'machine learning', 'feature selection', 'python'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas',
          'scikit-learn',
          'statsmodels',
          'matplotlib',
          'seaborn'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Framework :: Jupyter',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development :: Libraries :: Python Modules',
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