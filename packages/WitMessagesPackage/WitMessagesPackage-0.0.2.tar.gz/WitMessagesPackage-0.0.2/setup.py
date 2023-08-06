import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WitMessagesPackage",  # Replace with your own username
    version="0.0.2",
    author="Fernando del Corro",
    author_email="ferdelcorro@gmail.com",
    description="This repository will generate an interface to send emails, sms and WhatsApp to different companies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ferdelcorro/WitMessagesPackage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'phonenumbers==8.12.1',
        'requests==2.23.0',
        'sendgrid==6.1.3'
    ]
)
