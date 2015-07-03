from setuptools import setup


setup(
    name="gremlinrestclient",
    version="0.0.2",
    url="",
    license="MIT",
    author="davebshow",
    author_email="davebshow@gmail.com",
    description="Python client for Gremlin Server REST endpoint",
    long_description=open("README.txt").read(),
    packages=["gremlinrestclient", "tests"],
    install_requires=[
        "requests==2.7.0"
    ],
    test_suite="tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
