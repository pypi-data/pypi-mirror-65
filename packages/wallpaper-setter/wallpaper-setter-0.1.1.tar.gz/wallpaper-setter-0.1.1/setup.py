from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name="wallpaper-setter",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click>=7.1.1","sqlalchemy>=1.3.0","toml>=0.10.0","pywal>=3.3.0","easy_table>=0.0.4"],
    entry_points='''
        [console_scripts]
        wpsetter=wallpaper_setter.cli:cli
    ''',

    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',

    author="Douwe Hoekstra",
    author_email="douwe.hoekstra2512@gmail.com",
    description="Simple utility for managing wallpapers from the command-line",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dhoekstra/wallpaper-setter",
    keywords="wallpaper setter colors manager",
)
