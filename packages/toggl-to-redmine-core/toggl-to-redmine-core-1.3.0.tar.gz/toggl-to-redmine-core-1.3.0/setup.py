import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toggl-to-redmine-core",
    version="1.3.0",
    author="Eduardo Canellas",
    author_email="eduardocanellas@id.uff.br",
    description="Core package for the toggl_to_redmine import tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eduardocanellas/toggl-to-redmine-core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)