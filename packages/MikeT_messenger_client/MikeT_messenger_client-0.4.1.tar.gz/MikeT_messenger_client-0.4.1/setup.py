from setuptools import setup
from setuptools import find_packages

setup(
    name="MikeT_messenger_client",
    version="0.4.1",
    description="Messenger_client_part",
    author="machukhinktato",
    author_email="machukhinktato@mail.ru",
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
)
