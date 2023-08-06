from setuptools import setup, find_packages

setup(name="My_Server_Student",
      version="0.0.1",
      description="Messenger_Server",
      author="Student",
      author_email="user@user.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )

