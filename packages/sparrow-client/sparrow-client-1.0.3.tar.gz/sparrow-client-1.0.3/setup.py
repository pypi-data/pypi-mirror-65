import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sparrow-client", # Replace with your own username
    version="1.0.3",
    author="yeoseot",
    author_email="changyeon@peoplefund.co.kr",
    description="sparrow_client",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'redis==3.3.8',
        'requests==2.22.0',
    ]
)
