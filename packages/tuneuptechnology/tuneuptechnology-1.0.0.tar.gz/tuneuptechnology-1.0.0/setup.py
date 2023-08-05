import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = [
    'requests >= 1.0.0',
]

setuptools.setup(
      name='tuneuptechnology',
      version='1.0.0',
      description='The Python client library for the Tuneup Technology App.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/ncr4/tuneuptechnology-python',
      author='NCR4',
      author_email='justin@ncr4.com',
      license='MIT',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      install_requires=REQUIRES,
      python_requires='>=3.6',
)
