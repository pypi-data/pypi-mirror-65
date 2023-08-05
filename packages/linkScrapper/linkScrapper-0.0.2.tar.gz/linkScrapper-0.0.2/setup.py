import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linkScrapper", # Replace with your own username
    version="0.0.2",
    author="augustt0",
    author_email="bigeagleteam@gmail.com",
    description="With this package you can get all links inside a https link and retrieve them as an array",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/augustt0/linkScrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['beautifulsoup4'],
)