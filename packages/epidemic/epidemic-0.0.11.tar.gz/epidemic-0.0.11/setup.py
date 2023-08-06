from distutils.core import setup


setup(
  name = 'epidemic',
  packages = ['epidemic'],
  version = '0.0.11',
  license='MIT',
  description = 'This is a python library that can help predict when will next epidemic happen (relatively). MAY NOT BE ACCURATE',   # Give a short description about your library
  long_description='See detail description: https://epidemic.readthedocs.io',
  long_description_content_type="text/markdown",
  author = 'BOYUAN LIU',
  author_email = 'boyuanliu6@yahoo.com',
  url = 'https://github.com/boyuan12/epidemic',
  download_url = 'https://github.com/boyuan12/epidemic/archive/v0.0.8-alpha.tar.gz',
  keywords = ['epidemic', 'python', 'health'],
  install_requires=[
          'numpy',
          'matplotlib',
          'termcolor',
          'scikit-learn',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
  ],
)
