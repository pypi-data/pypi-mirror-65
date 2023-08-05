import setuptools;

with open("README.md", "r") as fh:
    long_description = fh.read();

setuptools.setup(
    name="sharpify",
    version="0.1.1",
    author="Ricki",
    author_email="",
    description="Turn the flask routing / architecture into Asp.Net Core like",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires = ["Flask"],
    license = "MIT",
    include_package_data = True
);


# python setup.py sdist bdist_wheel
# twine upload dist/sharpify-0.1.1-py3-none-any.whl dist/sharpify-0.1.1.tar.gz