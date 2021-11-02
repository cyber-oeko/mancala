import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mancala",
    version="1.0.0",
    author="Johannes Kopton",
    author_email="johannes@kopton.org",
    description="Online multiplayer Mancala game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyber-oeko/mancala",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "gui_scripts": ["mancala = mancala.gui_client:main"]
    },
    data_files = [
        ('share/applications/', ['mancala.desktop'])
    ],
    package_data={
        "mancala": ["style/*.qss", "assets/marbles/*.png", "assets/marbles_large/4.png", "assets/marbles_large/14.png"]
    },
    package_dir={"": "src"},
    packages=["mancala"],
    python_requires=">=3.7",
)
