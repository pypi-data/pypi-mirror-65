from setuptools import setup

print("got here")

setup(
    name="Example Python Package",
    version="1.0.2",
    description="An example Python package",
    url="https://example.com",
    author="matcaz",
    packages=["example"],
    include_package_data=True,
)
