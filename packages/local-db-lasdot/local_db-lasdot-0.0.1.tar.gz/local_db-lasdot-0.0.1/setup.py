import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='local_db-lasdot',
    version='0.0.1',
    author='Kelechi Ogudu',
    author_email='icheleck25@gmail.com',
    description='light weight package for populating mongo database and query it with energy data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Leko25/LocalDb.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.5'
)