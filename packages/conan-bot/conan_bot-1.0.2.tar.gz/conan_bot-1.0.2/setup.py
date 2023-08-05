from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='conan_bot',
    version='1.0.2',
    packages=find_packages('.'),
    url='https://github.com/nerakhon/conan-bot',
    license='MIT',
    author='Jan Paul',
    author_email='paulj@nerakhon.cz',
    entry_points={
        'console_scripts': ['conan-bot=conan_bot.bot:main'],
    },
    description='Bot for reporting conan exiles information on discord',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['discord', 'python-a2s'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
