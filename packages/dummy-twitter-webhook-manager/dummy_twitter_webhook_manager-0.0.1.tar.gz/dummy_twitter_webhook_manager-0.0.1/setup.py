import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dummy_twitter_webhook_manager",
    version="0.0.1",
    author="sammer sallam",
    author_email="samersallam92@gmail.com",
    description="A Python package help you when you want to reun a twitter bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Samer92",
    packages=["dummy_twitter_webhook_manager"],
    install_requires=["certifi==2020.4.5.1","chardet==3.0.4","idna==2.9","oauthlib==3.1.0",
                      "PySocks==1.7.1","requests==2.23.0","requests-oauthlib==1.3.0","six==1.14.0"
                      ,"tweepy==3.8.0","urllib3==1.25.8"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)