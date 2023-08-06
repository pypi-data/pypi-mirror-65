import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netlify_publish", # Replace with your own username
    version="0.0.3",
    author="Wassim Benzarti",
    author_email="m.wassim.benzarti@gmail.com",
    description="Publish to netlify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/commits-generation/netlify-publish",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
