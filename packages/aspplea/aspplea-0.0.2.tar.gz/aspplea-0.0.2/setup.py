import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name = "aspplea",
        version = "0.0.2",
        author = "Lea Hohmann",
        author_email = "lea.hohmann@outlook.de",
        description = "ASPP course project package 'Traveling Salesperson'",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/LeaHohmann/TravelingSalesperson",
        packages = setuptools.find_packages(),
        install_requires = [
            'numpy',
            'pandas'
        ],
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
        py_modules = [
            'salesman',
            'heuristic',
            'exact'
        ],
        python_requires = '>=3.4'
)

