from setuptools import setup, find_packages

setup(
    name="huchengzhen",
    version="0.0.1",
    keywords=("pip", "testpypi"),
    description="test pip module",
    long_description="test how to define pip module and upload to pypi",
    license="MIT",

    url="https://huchengzhen.com",  # your module home page, such as
    author="Hu Chengzhen",  # your name
    author_email="huchengzhen@gmail.com",  # your email

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
