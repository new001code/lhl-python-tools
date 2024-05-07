from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lhl-python-tools",
    version="0.0.1",
    author="new001code",
    author_email="lhl_creeper@163.com",
    description="A package for python dev",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/new001code/lhl-python-tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=["loguru~=0.7.2", "PyYAML~=6.0.1", "loguru-config~=0.1.0"],
)
