import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Avatar-Utils",
    version="1.0.5",
    author="Algorithmics of Complex System",
    author_email="artem.sementsov@gmail.com",
    description="Common utils for services in ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['avatar_utils', 'avatar_utils.logs'],
    install_requires=[
        'flask>=1.1.1',
        'flask-sqlalchemy>=2.3.2',
        'requests>=2.23.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
