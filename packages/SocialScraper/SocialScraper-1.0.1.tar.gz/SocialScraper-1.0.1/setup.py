import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SocialScraper", 
    version="1.0.1",
    author="Aravindha Hariharan",
    author_email="aravindha1234u@gmail.com",
    description="Social Scraper is a python tool meant for Detection of Child Predators/Cyber Harassers on Social Media",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aravindha1234u/SocialScraper",
    packages=setuptools.find_packages(),
    license='GPLv3+',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
    ],
    python_requires='>=3.6',
    install_requires=["requests","bs4","igql","urllib3","httplib2","oauth2","selenium","apiclient","google-api-python-client==1.5.5","bs2json","pprint","httplib2","oauth2client","jsonlib-python3","pyyaml"],
    console=["socialscraper.py"],
)

print("\nInstallation Successfull")
