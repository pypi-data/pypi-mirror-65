from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="sisenseautomation",
    version="0.0.1",
    description="Package for automating sisense tasks.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/cristhianmurcia182/sisense-automation",
    author="cmurcia",
    author_email="cmurcia@workforcelogiq.com",
    keywords="configuration core yaml ini json environment",
    license="MIT",
    packages=["sisenseautomation"],
    install_requires=["PyYAML", "azure-functions", "azure-storage-blob==2.1.0", "pytest"],
    include_package_data=True,
    zip_safe=False,
)