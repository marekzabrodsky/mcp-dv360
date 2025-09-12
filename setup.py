#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dv360-mcp-server",
    version="0.1.0",
    author="Claude Code",
    author_email="noreply@anthropic.com",
    description="A Model Context Protocol server for Google Display & Video 360 API integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/dv360-mcp-server-claude",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dv360-mcp-server=dv360_mcp_server.server:main",
        ],
    },
    keywords="mcp, model-context-protocol, google, dv360, display-video-360, advertising, ai, claude",
    project_urls={
        "Bug Reports": "https://github.com/your-username/dv360-mcp-server-claude/issues",
        "Source": "https://github.com/your-username/dv360-mcp-server-claude",
        "Documentation": "https://github.com/your-username/dv360-mcp-server-claude#readme",
    },
)