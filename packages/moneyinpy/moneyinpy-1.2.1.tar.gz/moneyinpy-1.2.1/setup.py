import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moneyinpy",
    version="1.2.1",
    author="Terry Hughes",
    author_email="terryhugheskirkcudbright@yahoo.co.uk",
    description="A simple accounting program",
    long_description=long_description,
    py_modules=["moneyinpy"],
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

