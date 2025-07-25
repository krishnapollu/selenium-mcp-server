#!/usr/bin/env python3
"""
Setup script for Selenium MCP Server

A Model Context Protocol server that brings Selenium WebDriver automation to AI assistants.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "A powerful Model Context Protocol (MCP) server that brings Selenium WebDriver automation to AI assistants."

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="selenium-mcp-server",
    version="1.1.6",
    author="Krishna Pollu",
    author_email="your.email@example.com",
    description="A powerful Model Context Protocol (MCP) server that brings Selenium WebDriver automation to AI assistants",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/krishnapollu/selenium-mcp-server",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "selenium-mcp-server=selenium_mcp_server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="selenium webdriver automation mcp model-context-protocol ai assistant",
    project_urls={
        "Bug Reports": "https://github.com/krishnapollu/selenium-mcp-server/issues",
        "Source": "https://github.com/krishnapollu/selenium-mcp-server",
        "Documentation": "https://github.com/krishnapollu/selenium-mcp-server#readme",
    },
) 