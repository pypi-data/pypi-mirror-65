import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Thomas Dewitte",
    author_email="thomasdewittecontact@gmail.com",

    name='surf_forecast',
    version='1.2.0',
    license="MIT",
    url='https://github.com/dewittethomas/surf-forecast',
    python_requires='>= 3.5',
    
    description='An api to fetch surf-forecast data',
    long_description=README,
    long_description_content_type="text/markdown",

    package_dir={"surf_forecast": "surf_forecast"},
    install_requires=["mechanize>=0.4.5", "beautifulsoup4>=4.8.2"],
    
    packages=setuptools.find_packages(),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)