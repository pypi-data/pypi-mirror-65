from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="egm",
    version="1.1.5",
    author="Mohit Bhatnagar",
    author_email="mohit@uplytics.com",
    keywords=['Plotly', 'evidence gap map', 'bubble graphs', 'interactive graphs'],
    description="A python package for plotting Evidence Gap Maps using Plotly",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://https://github.com/mb7419/egm/",
    packages=['egm'],
    install_requires=[
          'plotly',
          'pandas',
    ],
    zip_safe=False)