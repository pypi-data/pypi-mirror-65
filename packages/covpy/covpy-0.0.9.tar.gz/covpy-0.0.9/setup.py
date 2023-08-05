
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='covpy',  
     version='0.0.9',
     author="Pearse Doolin",
     author_email="pearsedoolin@gmail.com",
     description="A package for getting confirmed infection and death data on the 2019 coronavirus",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/pearsedoolin/covpy/",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    python_requires='>=3',
    install_requires=['numpy', 'pandas', 'xlrd'],


 )