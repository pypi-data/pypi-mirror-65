from setuptools import setup, find_packages



setup(
    name="eziocon", # Replace with your own username
    version="0.1",
    author="iyappan",
    author_email="iyappan.akp@gmail.com",
    description="A common package for doing basic operations over sql structured databases ",
    url="https://github.com/iyappan24/eziocon",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
         'pandas',
         'pymysql',
         'cx_Oracle',
          'json'
      ]
)


