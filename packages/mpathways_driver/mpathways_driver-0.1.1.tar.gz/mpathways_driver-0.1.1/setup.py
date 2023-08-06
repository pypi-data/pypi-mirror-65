from setuptools import setup

setup(
    name="mpathways_driver",
    version="0.1.1",
    packages=["mpathways_driver"],
    url="https://github.com/jamie-r-davis/mpathways_driver",
    license="MIT",
    author="Jamie Davis",
    author_email="jamjam@umich.edu",
    description="A wrapper around Selenium to enable automation in MPathways.",
    install_requires=["selenium==3.141.0", "urllib3==1.25.8"],
)
