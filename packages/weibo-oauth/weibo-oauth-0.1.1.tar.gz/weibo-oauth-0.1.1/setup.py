import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weibo-oauth",  # Replace with your own username
    version="0.1.1",
    author="zcq100",
    author_email="zcq100@gmail.com",
    description="新浪微博API封装",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zcq100/weibo-oauth",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
