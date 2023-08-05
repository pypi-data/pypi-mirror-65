import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IVAOWrapper",
    version="0.1.1",
    author="Tchekda",
    author_email="contact@tchekda.fr",
    description="Light Python 3 Wrapper for IVAO Network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tchekda/IVAOWrapper",
    project_urls={
        "Documentation": "https://tchekda.github.io/IVAOWrapper",
        "Source Code": "https://github.com/Tchekda/IVAOWrapper",
    },
    packages=setuptools.find_namespace_packages(include=["ivao.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
    ],
    python_requires='>=3.4',
    install_requires=['requests'],
    test_suite='tests'
)
