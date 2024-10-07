from setuptools import setup, find_packages

# Read the requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="port-commons",
    version="0.1.7",
    packages=find_packages(),
    install_requires=required,  # Use the list of requirements
    include_package_data=True,
    description="Common package for Port Scraping Project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/devnouiq/port-commons.git",
    author="FarAlpha Technologies",
    author_email="dev@nouiq.com",
    license="MIT",
)
