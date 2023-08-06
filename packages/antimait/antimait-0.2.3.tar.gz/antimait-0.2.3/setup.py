from setuptools import setup, find_packages  # type: ignore

with open("README.md", "r") as desc_file:
    desc = desc_file.read()


setup(
    name="antimait",
    version="0.2.3",
    description="antimait is a library made of tools to ease the implementation "
                "of IoT automation systems based on devices such as Arduino and ESP.",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="Gianmarco Marcello",
    author_email="g.marcello@antima.it",
    url="https://github.com/Antimait/antimait",
    python_requires=">=3.7",
    install_requires=["matplotlib", "pyserial", "typing_extensions"],
    packages=find_packages(exclude=["tests"]),
    scripts=["scripts/antimait_printer"]
)
