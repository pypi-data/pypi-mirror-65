from setuptools import setup, find_packages

setup(
    name='bsgen',
    version='0.2.2',
    description='BullshitGenerator',
    url='https://github.com/voidful/BullshitGenerator',
    author='Voidful',
    author_email='voidful.stack@gmail.com',
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_dir={'bsgen': 'bsgen'},
    package_data={
        'bsgen': ['data/*.json'],
    },
    install_requires=[
        "inquirer"
    ],
    entry_points={
        'console_scripts': ['bsgen=bsgen.generate:main']
    },
    zip_safe=True
)
