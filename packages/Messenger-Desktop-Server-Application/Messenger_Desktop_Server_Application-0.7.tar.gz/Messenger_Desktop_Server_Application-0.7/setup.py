from setuptools import setup, find_packages

setup(name="Messenger_Desktop_Server_Application",
      version="0.7",
      description="Messenger_Server",
      author="Dronkin Artem",
      author_email="adronkin@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'functools']
      )
