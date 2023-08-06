# для запуска py setup.py sdist bdist_wheel
from setuptools import setup, find_packages

setup(name="Mess_Server_al",
      version="0.0.1",
      description="Messenger_Server",
      author="Alena Vetrova",
      author_email="geekbr.alena.vetr@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
