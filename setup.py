from setuptools import setup, find_packages

# Read the requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="mypackage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=required,  # Use the list of requirements
    include_package_data=True,
    description="Common package for Port Scraping Project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/mypackage",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
)
