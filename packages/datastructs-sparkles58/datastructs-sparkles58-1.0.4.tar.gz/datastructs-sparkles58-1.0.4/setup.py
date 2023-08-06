import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datastructs-sparkles58", # Replace with your own username
    version="1.0.4",
    author="Ezra SB",
    author_email="ezzysuger717@gmail.com",
    description="Queues and trees.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sparklesunicorn/datastructs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
