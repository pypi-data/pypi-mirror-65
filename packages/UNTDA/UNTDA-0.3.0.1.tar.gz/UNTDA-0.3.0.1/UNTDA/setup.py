import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'UNTDA',
  version = '0.3.0.1',
  author = 'Isaac Zainea',
  author_email = 'isaaczainea@gmail.com',  
  description = 'paquete de aprendizaje de TDA - UNAL Colombia',
  url = 'https://github.com/izainea/UNATD', # use the URL to the github repo
  keywords = ['testing', 'ATD', 'TDA'],
  packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
