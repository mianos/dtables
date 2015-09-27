from setuptools import setup

setup(name='dtables',
      version='0.1',
      description='Python dtables mappper',
      url='https://github.com/mianos/dtables',
      author='Robbie Fowler',
      author_email='rfo@mianos.com',
      license='MIT',
      install_requires=['flask>=0.10', 'sqlalchemy>=0.9'],
      packages=['dtables'])
