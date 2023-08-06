import setuptools

# with open("README.md", 'r') as f:
#     long_description = f.read()


setuptools.setup(
    name = "siriusbackbone",
    version = "1.0.0",
    author = "sirius demon",
    author_email = "mory2016@126.com",
    description="Backbone in Pytorch",
    long_description="Backbone in Pytorch",
    long_description_content_type='text/markdown',
    url = "https://github.com/siriusdemon/private/hackaway",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)