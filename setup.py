import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requeriments.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='django-fbbot',
    version='0.1',
    install_requires=requirements,
    packages=find_packages(exclude=("djangobot",)),
    include_package_data=True,
    license='MIT License', 
    description='fbbot is a simple Django app to showcasing the Messenger Platform, make your facebook bot with Django',
    long_description=README,
    url='https://github.com/espacioAntonio/Django-messenger-platform-bot',
    author='espacioAntonio',
    author_email='espacio.antonio@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
)
