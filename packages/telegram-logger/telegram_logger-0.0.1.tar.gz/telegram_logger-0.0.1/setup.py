from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='telegram_logger',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/Beaxhem/telegram_logger',
    license='mit',
    author='beaxhem',
    author_email='senchukov02@gmail.com',
    description='Package allowing to log directly to Telegram',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
