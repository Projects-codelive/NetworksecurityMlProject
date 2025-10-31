''' The steup.py ia an essential part of packaging and distributing Python projects. It is used
by setuptools to define the configuration of project, such as its metadata, dependices and other
'''

from setuptools import setup, find_packages
''' find_package packages scan throughout the director and if any directory has __init__.py it willl consider it as 
package for ex- networksecurity has a __init__.py it will consider it as a package package and also the sub directory will 
 also be consider as package'''
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return a list of package requirements

    """
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # ignore the empty line and ignore -e.
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('No requirements.txt found')

    return requirement_lst

setup(
    name='networksecurity',
    version='0.0.1',
    author='Shyam Gupta',
    author_email='sg790540@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)
