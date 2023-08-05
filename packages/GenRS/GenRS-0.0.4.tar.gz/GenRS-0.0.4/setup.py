from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='GenRS',
    version='0.0.4',
    packages = find_packages(),
    author='Roberto Cedolin',
    author_email='roberto.cedo@gmail.com',
    url='https://pypi.org/project/GenRS/',
    license='LICENSE',
    description='A Generative learning-based Framework for Recommendation System algorithms',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
