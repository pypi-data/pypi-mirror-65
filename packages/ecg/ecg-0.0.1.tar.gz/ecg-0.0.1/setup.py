import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("version.txt", "r", encoding="utf8") as f:
    v_num = f.read().strip()

setuptools.setup(
    name="ecg",
    version=v_num,
    description="Test",
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    include_package_data=True,
    package_data={"ecg": ["*.png"],},
    url="https://your.url.com",
    author="Christian Baumann",
    author_email="your.name@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=["requests",],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["ecg=ecg.main:main"],},
)
