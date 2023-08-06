import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Self_Quarantine", # Replace with your own username
    version="0.0.1",
    author="Abhinav Singh",
    author_email="abhinav.coder@gmail.com",
    description="self tracking application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhinavclemson/Self_Quarantine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
