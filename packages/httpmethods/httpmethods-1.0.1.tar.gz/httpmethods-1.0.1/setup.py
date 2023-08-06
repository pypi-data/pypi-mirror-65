import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='httpmethods',
    version='1.0.1',
    license='MIT',
    description='HTTP methods that python supports',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Braian Staimer',
    author_email='braianflorian@gmail.com',
    url='https://github.com/staimerapi/httpmethods',
    packages=setuptools.find_packages(),
    download_url='https://github.com/staimerapi/httpmethods/archive/1.0.1.tar.gz',
    keywords=['HTTP', 'HTTP REQUEST', 'REQUESTS METHODS'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
