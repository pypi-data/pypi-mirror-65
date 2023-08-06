import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
setuptools.setup(
    name='qa-helper',
    version='0.1',
    scripts=['qa-helper'],
    author="YZ",
    author_email="mohammad.you92@gmail.com",
    description="Tools for write automation test easily",
    # url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
)
