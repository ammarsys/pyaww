# type: ignore

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaww",
    version="1.0.0",
    author="ammarsys",
    author_email="amarftw1@gmail.com",
    description="An API wrapper around the PythonAnywhere's API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ammarsys/pyaww/",
    project_urls={
        "Bug Tracker": "https://github.com/ammarsys/pyaww/issues",
        "Documentation": "https://pyaww-docs.vercel.app/",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=["aiohttp==3.8.1"],
    python_requires=">=3.9",
    license="MIT",
)
