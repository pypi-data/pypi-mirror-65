from distutils.core import setup
setup(
    name="test_python_package_1",
    version="1.0.2",
    py_modules=["test_python_package_1"],
    author="lfalanga",
    author_email="lfalanga@gmail.com",
    url="https://github.com/lfalanga/test_python_package_1",
    description="My first Python package.",
    packages=["package_example", "package_example.subpackage_example"],
    )
