from setuptools import setup

# with open("README.md", "r") as re:
#     long_description = re.read()

setup(
    name='teranetpracticum',
    version='0.1.1',
    author='kaiyuwang',
    author_email='kaiyuwangwork@gmail.com',
    url='https://github.com/kaiyuwang-work',
    description=u'teranet practicum package test',
    scripts=["__init__.py"],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'national=teranetpracticum:national',
            'bc=teranetpracticum:bc'
        ]
    }
)