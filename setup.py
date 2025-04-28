from setuptools import setup, find_packages

setup(
    name="llm-pentest",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "praw>=7.7.1",
        "PyGithub>=2.1.1",
        "arxiv>=1.4.7",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.10",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for pentesting LLM endpoints",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-pentest",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "llm-pentest=llm_pentest.core.cli:main",
            "llm-monitor=llm_pentest.core.monitor_cli:main",
        ],
    },
) 