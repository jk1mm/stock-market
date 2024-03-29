from setuptools import find_packages, setup

setup(
    name="stock_market",
    version="1.3.2",
    description="Modules related to stock market model.",
    author="Josh Kim",
    author_email="joshkim47@gmail.com",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=[
        "pandas>=1.3.5,<2.0.0",
        "numpy>=1.21.5,<2.0.0",
        "pandas-datareader==0.10.0,<1.0.0",
        "bs4>=0.0.1",
        "requests>=2.26.0,<3.0.0",
        "plotly>=5.4.0,<6.0.0",
        "praw>=7.5.0,<8.0.0",
        "prawcore>=2.3.0,<3.0.0",
        "pyspellchecker==0.6.2,<1.0.0",
        "python-dotenv",
        "nltk>=3.6.5,<4.0.0",
        "finviz>=1.4.3,<2.0.0",
    ],
    include_package_data=True,
    python_requires=">=3.6",
)
