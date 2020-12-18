from setuptools import setup, find_packages


setup(
    name="package_template",
    version="1.0.0",
    description="Package template",
    author="Josh Kim",
    author_email="joshkim47@gmail.com",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=[""],
    python_requires=">=3.6",
)
