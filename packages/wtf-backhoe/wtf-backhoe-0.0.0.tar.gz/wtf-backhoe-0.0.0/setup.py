from setuptools import find_packages, setup

REQUIREMENTS = {"install": [], "develop": [], "test": []}
README_CONTENTS: str

with open("README.md", "r") as readme:
    README_CONTENTS = readme.read()

setup(
    name="wtf-backhoe",
    version="0.0.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    author="Bulat Bochkariov",
    author_email="wtf-backhoe@bulat.bochkariov.com",
    description="Bulk-insert for WTForms",
    long_description=README_CONTENTS,
    long_description_content_type="text/markdown",
    url="https://github.com/bulatb/wtf-backhoe",
    project_urls={
        "Source": "https://github.com/bulatb/wtf-backhoe",
        "Issues": "https://github.com/bulatb/wtf-backhoe/issues",
    },
    install_requires=REQUIREMENTS["install"],
    extras_require={
        "develop": set(REQUIREMENTS["develop"] + REQUIREMENTS["test"]),
        "test": REQUIREMENTS["test"],
    },
    python_requires=">=3.5",
    keywords="wtforms bulk insert upload import",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
