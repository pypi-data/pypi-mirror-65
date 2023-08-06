import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commit-generation-datasets", # Replace with your own username
    version="0.0.1",
    author="Wassim Benzarti",
    author_email="m.wassim.benzarti@gmail.com",
    description="Dataset downloader for the commits generation project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/commits-generation/commits-datasets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)