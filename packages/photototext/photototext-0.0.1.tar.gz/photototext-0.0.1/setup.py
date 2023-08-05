import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="photototext",
    version="0.0.1",
    author="peler",
    author_email="2975972646@qq.com",
    description="This is a module that can turn a picture into a pattern of letters and symbols.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/photototext/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)