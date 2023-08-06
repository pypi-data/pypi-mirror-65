import setuptools

setuptools.setup(
    name="holidays_es",
    version="1.0.1",
    url="https://github.com/rsolanoweb/holidays-es",
    author="Rubén Solano",
    author_email="rubensoljim@gmail.com",
    description="Public holidays in Spain from 2006 to now.",
    long_description=open("README.rst").read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
