import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='pkg',
    version='0.2',
    author='João Moreira de Sá Coutinho',
    author_email='joao.moreiradsc@gmail.com',
    description='Python scripts dealing with software packages used in building applications and systems',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/joaomdsc/pkg',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7.3',
)
