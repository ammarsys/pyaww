import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyanywherewrapper",
    version="0.0.3",
    author="ammarsys",
    author_email="",
    description="A simple API wrapper around the pythonanywhere's API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ammarsys/pyanywhere-wrapper/",
    project_urls={
        "Bug Tracker": "https://github.com/ammarsys/pyanywhere-wrapper/issues",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pyanywhere"},
    install_requires=[
        'requests==2.25.1'
    ],
    python_requires=">=3.6",
    license='MIT'
)
