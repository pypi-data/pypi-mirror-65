import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoSubtitles",  # Replace with your own username
    version="0.0.1",
    author="AndrewYq",
    author_email="hfyqstar@163.com",
    description="Auto-generates subtitles for any video !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yqstar/AutoSubtitles",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
