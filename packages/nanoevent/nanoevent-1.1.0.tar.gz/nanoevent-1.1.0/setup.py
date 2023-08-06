import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = []
test_deps = ['pytest']

setuptools.setup(
    name="nanoevent",
    version="1.1.0",
    author="Berry Langerak",
    author_email="berry.langerak@gmail.com",
    description="Nanoevent is a terrifically small and simple event bus implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/berry-langerak/nanoevent",
    packages=['nanoevent'],
    install_requires=dependencies,
    tests_require=test_deps,
    extras_require={
        'test': test_deps
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
)