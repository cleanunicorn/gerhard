from setuptools import setup

setup(
    name="gerhard",
    version="0.1",
    py_modules=["gerhard"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        gerhard=gerhard.main:cli
    """,
)
