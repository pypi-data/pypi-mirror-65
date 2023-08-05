import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="portfoliotools", # Replace with your own username
    version="1.0.7",
    author="Rahul Jain",
    author_email="rahulspsec@gmail.com",
    description="Utils to fetch and analyze portoflio of stocks, index, mutual funds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rahulspsec/portfoliotools/",
    packages=setuptools.find_packages(),
    #package_dir = {'portfoliotools/screener':'screener'},
    #namespace_packages=['screener'],
    install_requires=[
        "beautifulsoup4",
        "pandas",
        "numpy",
        "mftool",
        "requests",
        "pandas-datareader",
        #"TA-Lib",
        "plotly",
        "stocktrends",
        "scipy",
        "scikit-learn",
        "seaborn",
        "statsmodels",
        "nsepy",
        "nsetools",
    ],
    classifiers=[
	    'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6',
    zip_safe=False,
)