import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='envtypes',
    version='0.2.1',
    author='YazeeMe',
    author_email='contact@yazee.me',
    description='Sort env types and return the needed one',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ionut-badea/env-types',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['python-dotenv']
)
