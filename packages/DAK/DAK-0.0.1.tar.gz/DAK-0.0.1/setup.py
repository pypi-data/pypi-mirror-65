import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DAK", # Replace with your own username
    version="0.0.1",
    author="Feng Bao",
    author_email="fbao0110@gmail.com",
    description="Explaining the genetic causality for complex diseases by deep association kernel learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fbaothu/DAK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)