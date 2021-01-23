from setuptools import setup

version = "1.0.0"

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", encoding="utf-8") as req_file:
    requirements = req_file.read().splitlines()

setup(
    name="imperialbin",
    version=version,
    description=(
        "bruh"
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Hexiro",
    author_email="realhexiro@gmail.com",
    url="https://github.com/Hexiro/",
    packages=["imperialbin"],
    python_requires=">=3",
    install_requires=requirements,
    license="CC0",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: CC0 License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "Python",
        "Python3"
    ],
)
