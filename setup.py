from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="nexuslang",
    version="5.3.0",
    description="The first bilingual (Spanish/English) programming language with built-in AI, database and web generation. Zero dependencies.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Lucas",
    license="MIT",
    py_modules=["nexuslang"],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["nexus=nexuslang:main", "nexuslang=nexuslang:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Interpreters",
        "Natural Language :: Spanish",
        "Natural Language :: English",
    ],
)
