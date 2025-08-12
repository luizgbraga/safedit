import os

from setuptools import find_packages, setup


def get_long_description():
    """Get long description from README.md if it exists."""
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "A collaborative file editor with real-time synchronization using CRDT"


setup(
    name="safedit",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.20.0",
        "watchdog>=3.0.0",
        "python-socketio>=5.8.0",
        "typer>=0.9.0",
        "python-multipart>=0.0.6",
    ],
    entry_points={
        "console_scripts": [
            "safedit=safedit.cli:app",
        ],
    },
    include_package_data=True,
    package_data={
        "safedit": ["static/*", "static/**/*"],
    },
    python_requires=">=3.8",
    author="Luiz Braga",
    author_email="your.email@example.com",
    description="A collaborative file editor with real-time synchronization using CRDT",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/luizgbraga/safedit",
    project_urls={
        "Bug Reports": "https://github.com/luizgbraga/safedit/issues",
        "Source": "https://github.com/luizgbraga/safedit",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Editors",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="editor collaborative real-time crdt websocket",
)
