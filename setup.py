"""Setup configuration for IRC Chat Client."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="irchat",
    version="1.1.0",
    author="IRC Chat Client Contributors",
    author_email="",
    description="A lightweight, thread-safe IRC (Internet Relay Chat) client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neoastra303/irchat",
    project_urls={
        "Bug Tracker": "https://github.com/neoastra303/irchat/issues",
        "Documentation": "https://github.com/neoastra303/irchat#readme",
        "Source Code": "https://github.com/neoastra303/irchat",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Typing :: Stubs Only",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12",
            "pylint>=2.9",
            "flake8>=3.9",
            "mypy>=0.910",
            "black>=21.6",
            "isort>=5.9",
            "bandit>=1.7",
            "safety>=1.10",
            "coverage>=5.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "irchat=run:main",
        ],
    },
    keywords=[
        "irc",
        "chat",
        "client",
        "protocol",
        "internet-relay-chat",
        "cli",
        "terminal",
    ],
)
