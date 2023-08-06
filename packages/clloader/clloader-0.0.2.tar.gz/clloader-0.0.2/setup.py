import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clloader",
    version="0.0.2",
    author="Arthur DOuillard",
    author_email="ar.douillard@gmail.com",
    description="A DataLoader library for Continual Learning in PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurdouillard/continual_loader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
