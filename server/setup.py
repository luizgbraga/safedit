from setuptools import find_packages, setup

setup(
    name="safedit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "watchdog",
        "python-socketio",
        "typer",
    ],
    entry_points={
        "console_scripts": [
            "safedit=safedit.cli:app",
        ],
    },
    include_package_data=True,
    package_data={
        "safedit": ["static/**/*"],
    },
    author="Your Name",
    description="Multi-client collaborative file editor with CRDT demo",
    long_description=open("README.md").read()
    if __import__("os").path.exists("README.md")
    else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/safedit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
