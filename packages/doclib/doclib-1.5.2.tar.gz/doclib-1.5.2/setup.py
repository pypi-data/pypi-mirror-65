import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='doclib',
     version='1.5.2',
     scripts=['doclib/__init__.py'] ,
     author="DoctorNumberFour",
     author_email="miloszecket@gmail.com",
     description="A chatbot library for euphoria.io.",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://gitlab.com/DoctorNumberFour/DocLib",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: OS Independent",
     ],
     install_requires=['websocket-client', 'websockets', 'attrdict'],
     python_requires = '>=3.6'
 )
