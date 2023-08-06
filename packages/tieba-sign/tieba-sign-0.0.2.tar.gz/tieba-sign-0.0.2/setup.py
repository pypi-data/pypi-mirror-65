import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tieba-sign",  # Replace with your own username
    version="0.0.2",
    author="zcq100",
    author_email="zcq100@gmail.com",
    description="贴吧自动签到",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zcq100/tieba-sign",
    packages=setuptools.find_packages(),
    entry_points={
      'console_scripts':[
          'tieba-sign=tieba.sign:main',
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
