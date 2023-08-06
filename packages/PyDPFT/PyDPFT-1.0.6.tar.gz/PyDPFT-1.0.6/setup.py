import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyDPFT", # Replace with your own username
    version="1.0.6",
    author="Ding Ruiqi",
    author_email="416640656@qq.com",
    description="A package for density potential functional theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tesla-cat/PyDPFT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)