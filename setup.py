''' The steup.py ia an essential part of packaging and distributing Python projects. It is used
by setuptools to define the configuration of project, such as its metadata, dependices and other
'''
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return a list of package requirements
    """
    # reading requirement.txt
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read the line from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                # .strip() removes the empty spaces
                requirement = line.strip()
                # ignore the empty line and -e.
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print('requirements.txt not found')
    return requirement_list

# Setup the meta data
setup(
    name='networksecurityss',
    version='0.0.1',
    author='Shyam Gupta',
    author_email='sg790540@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)