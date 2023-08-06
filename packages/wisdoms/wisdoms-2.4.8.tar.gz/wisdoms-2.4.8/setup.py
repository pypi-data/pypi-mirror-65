# Created by Q-ays.
# whosqays@gmail.com


import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="wisdoms",
    version="2.4.8",
    author="tzxd group",
    author_email="975663670@qq.com",
    description="存档添加order id，pg添加模糊查询，es添加terms查询",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/soft-project/wisdom-lib",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyYaml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
