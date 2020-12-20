from setuptools import setup, find_packages


setup(
    name="stock_market",
    version="1.0.0",
    description="Modules related to stock market analysis.",
    author="Josh Kim",
    author_email="joshkim47@gmail.com",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=[
        "pandas>=1.1.5",
        "pandas-datareader>=0.9.0",
        "bs4>=0.0.1",
        "requests>=2.25.1",
    ],
    python_requires=">=3.6",
)
