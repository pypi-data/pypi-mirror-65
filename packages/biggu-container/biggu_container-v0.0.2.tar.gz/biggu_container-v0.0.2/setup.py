from distutils.core import setup

setup(
    name = 'biggu_container',
    packages = ['biggu_container'],
    version = 'v0.0.2',
    exclude=["test"],
    description = 'IoC for python projects',
    author = 'Eduardo Salazar',
    author_email = 'eduardosalazar89@hotmail.es',
    url = 'https://github.com/esalazarv/biggu-container.git',
    download_url = 'https://github.com/esalazarv/biggu-container/archive/v0.0.2.zip',
    keywords = ['biggu_container', 'IoC', 'dependencies', 'injection', 'resolution'],
    license="MIT",
    classifiers = [
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=[],
)