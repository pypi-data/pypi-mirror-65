import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='oom',
    version='0.1.0',
    author='Eduard Konanau',
    author_email='aduard.kononov@gmail.com',
    description="Prevents freezing of your machine when it's running out of RAM",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/aduard.kononov/oom',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
