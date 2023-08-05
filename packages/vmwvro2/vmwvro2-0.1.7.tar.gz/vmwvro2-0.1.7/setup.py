import setuptools
with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open("VERSION", "r") as fh:
    version = fh.readline().rstrip()
    #version = "0.1.4"


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='vmwvro2',
      version=version,
      description='REST lib for VMWARE vRO',
      url='http://github.com/JoseIbanez/vmwvro2',
      author='Jose Ibanez',
      author_email='ibanez.j@gmail.com',
      license="MIT License",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      install_requires=install_requires,
      include_package_data=True,
      classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
      ],
      zip_safe=False)
