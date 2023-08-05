import setuptools

setuptools.setup(
    name="yelp-common",
    version="1.1.7",
    author="Sam Kim",
    author_email="samkim90274@gmail.com",
    url="https://github.com/sampromises/yelp-common",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=["bs4", "requests", "dateparser",],
    python_requires=">=3.8",
)
