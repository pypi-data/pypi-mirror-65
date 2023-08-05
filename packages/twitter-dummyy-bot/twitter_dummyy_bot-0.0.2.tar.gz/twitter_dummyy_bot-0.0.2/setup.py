import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitter_dummyy_bot",
    version="0.0.2",
    author="sammer sallam",
    author_email="samersallam92@gmail.com",
    description="A Python package help you when you want to reun a twitter bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Samer92",
    packages=["twitter_dummyy_bot"],
    install_requires=["boto3==1.12.19","botocore==1.15.19",
                      "certifi==2019.11.28","chardet==3.0.4","click==7.1.1",
                      "docutils==0.15.2","emojis==0.5.1",
                      "Flask==1.1.1","idna==2.9",
                      "idna==2.9","itsdangerous==1.1.0",
                      "Jinja2==2.11.1","jmespath==0.9.5","langdetect==1.0.8","MarkupSafe==1.1.1",
                      "numpy==1.18.1","oauthlib==3.1.0","pandas==0.25.3",
                      "PySocks==1.7.1","python-dateutil==2.8.1","python-dotenv==0.12.0",
                      "pytz==2019.3","requests==2.23.0","requests-oauthlib==1.3.0",
                      "s3transfer==0.3.3","six==1.14.0","tweepy==3.8.0",
                      "urllib3==1.25.8","Werkzeug==1.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)