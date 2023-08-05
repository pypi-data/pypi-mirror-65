import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='one-line',
    version='0.1.3b',
    description='Make every step oneLine.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas',
        'seaborn',
        'scipy',
        'scikit-learn'
    ],
    packages=setuptools.find_packages(),
    author='Zeesain Tsui',
    author_email='clarenceehsu@163.com',
    url='https://github.com/clarenceehsu/oneLine',
    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)