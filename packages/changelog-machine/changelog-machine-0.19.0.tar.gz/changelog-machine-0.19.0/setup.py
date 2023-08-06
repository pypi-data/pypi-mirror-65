import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="changelog-machine",
    version="0.19.0",
    author="Ben Antony",
    author_email="antony@greenhalos.lu",
    description="A tool to generate changelogs integrated in a pull/merge request workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greenhalos/changelog-machine",
    packages=["changelog_machine"],
    scripts=["bin/changelog-machine"],
    # entry_points={
    #     'console_scripts': [
    #         'changelog-machine = changelog-machine.__main__:main'
    #     ]
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["PyYAML>=5.3.1"],
    python_requires=">=3.6",
)
