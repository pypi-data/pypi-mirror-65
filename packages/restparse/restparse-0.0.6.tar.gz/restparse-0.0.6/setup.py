import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="restparse",
    version="0.0.6",
    packages=setuptools.find_packages(),
    author="Julian Nash",
    author_email="julianjamesnash@gmail.com",
    description=
    "A simple, lightweight parser and validator for RESTful HTTP requests",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="flask django request parser json rest",
    url="https://github.com/Julian-Nash/restparse",
    project_urls={
        "Bug Tracker": "https://github.com/Julian-Nash/restparse",
        "Documentation": "https://github.com/Julian-Nash/restparse",
        "Source Code": "https://github.com/Julian-Nash/restparse",
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
