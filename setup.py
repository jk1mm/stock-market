from setuptools import find_packages, setup

setup(
    name="stock_market",
    version="1.2.1.1",
    description="Modules related to stock market model.",
    author="Josh Kim",
    author_email="joshkim47@gmail.com",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=[
        "pandas>=1.1.5",
        "numpy>=1.19.4",
        "pandas-datareader==0.9.0",
        "bs4>=0.0.1",
        "requests>=2.25.1",
        "plotly>=4.14.1",
        "praw==7.1.4",
        "prawcore>=1.5.0",
        "pyspellchecker==0.5.6",
        "python-dotenv",
        "nltk==3.5",
    ],
    include_package_data=True,
    python_requires=">=3.6",
)
