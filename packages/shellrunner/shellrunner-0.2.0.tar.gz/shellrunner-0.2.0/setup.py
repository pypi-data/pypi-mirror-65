from setuptools import setup, find_packages

with open("README.md") as fin:
    description = fin.read()

setup_args = dict(
    name='shellrunner',
    version='0.2.0',
    entry_points={
        'console_scripts': ['shellrunner=shellrunner.shellrunner:main']
    },
    author="Daniel Trugman",
    author_email="dtrugman@gmail.com",
    description="Speed up your shell activity",
    long_description=description,
    keywords=['shell', 'runner'],
    url="https://github.com/dtrugman/shellrunner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
