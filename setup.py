from setuptools import setup, find_packages

setup(
    name="file-merger",
    version="0.1.0",
    description="A Streamlit web application for merging CSV or Excel files based on user-selected columns.",
    author="Brandon Yach",
    author_email="byach@teamworks.com",
    url="[Repository URL, e.g., https://github.com/your-repo/file-merger]",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit==1.38.0",
        "pandas==2.2.3",
        "openpyxl==3.1.5",
        "pytest==8.3.3",
        "rapidfuzz==3.10.0",
        "watchdog==5.0.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)