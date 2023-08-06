from setuptools import find_packages
from distutils.core import setup

def get_version():
    return open('version.txt', 'r').read().strip()

setup(
    author='Vinicius Languer',
    author_email='vinicius@lojaspompeia.com.br',
    description='Pacote de consumo da Plug Boleto',
    license='MIT',
    name='lins_plugboleto',
    packages=find_packages(),
    url='https://bitbucket.org/grupolinsferrao/pypck-lins-plugboleto/',
    version=get_version(),
    zip_safe=False
)