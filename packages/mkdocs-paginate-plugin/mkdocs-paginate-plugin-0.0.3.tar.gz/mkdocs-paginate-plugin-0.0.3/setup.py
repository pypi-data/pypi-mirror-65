from setuptools import setup, find_packages

setup(
    name='mkdocs-paginate-plugin',
    version='0.0.3',
    description="Mkdocs paginate plugin",
    url="https://github.com/kubilus1/mkdocs-paginate-plugin",
    author='Matt Kubilus',
    install_requires=[
        'mkdocs>=0.17',
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': [
            'paginate = paginate.plugin:PaginatePlugin'
        ]
    }
)
