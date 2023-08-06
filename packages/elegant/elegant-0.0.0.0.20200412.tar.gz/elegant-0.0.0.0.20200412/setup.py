import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elegant",
    version="0.0.0.0.20200412",
    maintainer="",
    maintainer_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["elegant"],
    install_requires=['numpy', 'pillow'],
    # entry_points={
    #     'console_scripts': [
    #         'douyin_image=douyin_image:main'
    #     ],
    # },
    # classifiers=(
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ),
)
