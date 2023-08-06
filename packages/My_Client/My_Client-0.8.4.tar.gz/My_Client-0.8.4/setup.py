from setuptools import setup, find_packages

setup(name="My_Client",
      version="0.8.4",
      description="Messenger_Client",
      author="Ivan Ivanov",
      author_email="user@rt.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
