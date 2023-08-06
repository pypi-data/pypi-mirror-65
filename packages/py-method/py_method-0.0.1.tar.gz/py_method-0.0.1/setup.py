import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_method", # Replace with your own username
    version="0.0.1",
    author="John Ward",
    author_email="realjohntward@gmail.com",
    description="A pythonic interface to the Method CRM's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realjohnward/py-method",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)