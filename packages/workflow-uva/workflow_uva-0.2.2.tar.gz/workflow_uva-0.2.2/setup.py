import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='workflow_uva',  

     version='0.2.2',

     author="Jasper van der Heide",

     author_email="jaspervdh96@hotmail.com",

     description="A workflow for Canvas and Nbgrader",
	 install_requires=[
"beautifulsoup4>=4.7.1",
"canvasapi>=0.12.0",
"ipython>=6.2.1",
"ipywidgets>=7.4.2",
"matplotlib>=2.2.2",
"nbconvert>=5.5.0",
"nbgrader>=0.6.1",
"nbstripout>=0.3.6",
"numpy>=1.16.4",
"pandas>=1.0.1",
"requests>=2.22.0",
"seaborn>=0.9.0",
"tqdm>=4.32.2",
"traitlets>=4.3.2"
],

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/jaspervdh96/Workflow",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",
		 "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"

     ],

 )
