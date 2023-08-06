import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylorem",
    version="1.2",
    packages=setuptools.find_packages(),
    author="Julian Nash",
    author_email="julianjamesnash@gmail.com",
    description="A Python lorem ipsum generator",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="lorem ipsum placeholder dummy text generator",
    url="https://github.com/Julian-Nash/pylorem",
    include_package_data=True,
    project_urls={
        "Bug Tracker": "https://github.com/Julian-Nash/pylorem",
        "Documentation": "https://github.com/Julian-Nash/pylorem",
        "Source Code": "https://github.com/Julian-Nash/pylorem",
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)