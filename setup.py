from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
        name = "pytermvis",
        version = "0.2",
        description = "Python Terminal Audio Visualizer",
        long_description=readme(),
        url = "https://github.com/bharris6/pytermvis",
        author = "Brian Harrison",
        author_email = "harrison.brian.d@gmail.com",
        license = "MIT",
        packages = ["pytermvis"],
        install_requires = [
            "numpy",
            "scipy",
            "soundcard",
        ],
        entry_points = {
            'console_scripts': ['pytermvis=pytermvis.run:main'],
        },
        include_package_data = True,
        zip_safe = False
    )
