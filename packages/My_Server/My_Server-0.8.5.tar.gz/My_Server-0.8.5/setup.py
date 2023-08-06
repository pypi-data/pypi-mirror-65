from setuptools import setup, find_packages

setup(name="My_Server",
      version="0.8.5",
      description="Messenger_Server",
      author="Ivan Ivanov",
      author_email="user@rt.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
