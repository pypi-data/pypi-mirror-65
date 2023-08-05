from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRED_PACKAGES = [
    'google-auth',
    'firebase-admin'
]

setup(
    name='vaknl-user',
    description='User class that defines a user based on clickstream data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.0.6',
    url='https://github.com/vakantiesnl/vaknl-PyPi.git',
    author='Merijn van Es',
    author_email='merijn.vanes@vakanties.nl',
    keywords=['vaknl', 'pip'],
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=REQUIRED_PACKAGES
)
