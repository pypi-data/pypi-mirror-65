

# setup.py

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="baddfish-my-lambdata-13",
    version="1.0",
    author="Tony Maddalone",
    author_email="tjmaddalonec@gmail.com",
    description="For example purposes",
    long_description=long_description,
    long_description_content_type="text/markdown", # required if using a md file for long desc
    license="MIT",
    url="https://github.com/baddfish/my-lambdata-13",
    #keywords="",
    packages=find_packages() # ["my_lambdata"]
)