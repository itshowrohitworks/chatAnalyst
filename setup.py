from setuptools import setup, find_packages

setup(
    name="chatAnalyst",
    version="0.1.0",
    author="Rohit Shrivastava",
    author_email="therohitshrivastava@gmail.com",
    description="End-to-end ML system to predict expected donation amount for live streams",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
)