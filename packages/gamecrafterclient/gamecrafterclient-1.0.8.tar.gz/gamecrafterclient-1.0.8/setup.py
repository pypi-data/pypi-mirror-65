from setuptools import setup, find_packages

setup(
    name = "gamecrafterclient",
    version = "1.0.8",
    author = "Oliver Barnum",
    author_email = "oliverbarnum32@gmail.com",
    description = "Python API client for the game crafter.",
    url = "https://github.com/TheNextGuy32/gameCrafterClient",
    packages=find_packages(),
    install_requires=["tabulate", "asyncio","aiofile","aiohttp"],
    download_url="https://github.com/TheNextGuy32/gameCrafterClient/archive/1.0.4.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)