from setuptools import setup, find_packages

setup(name="AASMessenger_Client",
      version="1.0.1",
      description="Messenger_Client",
      author="Anton Sobolev",
      author_email="antony.sobolev@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
