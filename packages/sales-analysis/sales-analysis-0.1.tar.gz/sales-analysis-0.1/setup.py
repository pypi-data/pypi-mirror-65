from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def setup_package():
    setup(
        name='sales-analysis',
        version='0.1',
        author='Joseph Moorhouse',
        license=license,
        description='A sales analysis package for an imaginary e-shop',
        long_description_content_type="text/markdown",
        long_description=long_description,
        packages=find_packages(include=["sales_analysis", "sales_analysis.*"]),
        url="https://github.com/jbmoorhouse/sales_analysis",
        install_requires=[
            "flask>=1.1.1",
            "pytest",
            "pandas>=1.0.0",
            "pytest-flask>=1.0.0"
        ],
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
    )

if __name__ == "__main__": 
    setup_package()