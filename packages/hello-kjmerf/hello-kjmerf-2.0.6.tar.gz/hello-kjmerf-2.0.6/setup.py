import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="hello-kjmerf",
    version="2.0.6",
    author="Kevin Merfeld",
    author_email="kevinjmerfeld@gmail.com",
    description="A package that says hello to kjmerf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kjmerf/hello_kjmerf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
