from setuptools import setup, find_packages

setup(
  name='mvb',
  version='0.1.4',
  author='Michael Van Beek',
  author_email='michaelsvanbeek@gmail.com',
  url='https://github.com/michaelsvanbeek/mvb_py',
  packages=[
    'mvb',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities'
  ],
  install_requires=['IPython','pandas','papermill']
)
