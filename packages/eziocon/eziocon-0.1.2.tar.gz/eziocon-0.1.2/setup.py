from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup(
    name="eziocon", # Replace with your own username
    version="0.1.2",
    license = "MIT",
    author="iyappan",
    author_email="iyappan.akp@gmail.com",
    description="A common package for doing basic operations over sql structured databases ",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/iyappan24/eziocon",
    keywords = ['mysql python wrapper','oracle python wrapper','cx_oracle wrapper','pymysql wrapper','python sql sdk'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
         'pandas',
         'pymysql',
         'cx_Oracle'
      ]
)


