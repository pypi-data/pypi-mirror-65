import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="certimaker", # Replace with your own username
    version="0.0.1",
    author="Doctor Wu",
    author_email="277500223@qq.com",
    description="A package used to make word certificate easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwuch/certimaker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)