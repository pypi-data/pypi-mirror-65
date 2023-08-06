import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stackmod",
    version="0.0.1",
    author="Midriaz",
    author_email="scome@inbox.ru",
    description="Stacking for machine learning",
    url="https://github.com/Midriaz/stackmod",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)
