from setuptools import setup, find_packages


setup(
    name="demo",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    license="Not Open Source",
    entry_points={
        "console_scripts": [
            "demo = cli.demo:main",
        ]
    },
)
