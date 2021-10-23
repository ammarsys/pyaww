import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaww",
    version="0.0.4",
    author="ammarsys",
    author_email="amarftw1@gmail.com",
    description="A simple API wrapper around the pythonanywhere's API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ammarsys/pyaww/",
    project_urls={
        "Bug Tracker": "https://github.com/ammarsys/pyaww/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    packages=["pyaww"],
    install_requires=["typing_extensions==3.10.0.0", "requests==2.25.1"],
    python_requires=">=3.6",
    license="MIT",
)
