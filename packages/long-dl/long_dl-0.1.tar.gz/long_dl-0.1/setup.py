from distutils.core import setup
setup(
  name = 'long_dl',
  packages = ['long_dl'],
  version = '0.1',
  license='MIT',
  description = 'first dl lib by LongLH',
  author = 'LongLH',
  author_email = 'lehoanglong95@gmail.com',
  url = 'https://github.com/lehoanglong95/long_dl',
  download_url = 'https://github.com/lehoanglong95/long_dl/archive/0.1.tar.gz',
  keywords = ['deep_learning', 'pytorch', 'regression_evaluation_metrics'],
  install_requires=[
          'torch',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)