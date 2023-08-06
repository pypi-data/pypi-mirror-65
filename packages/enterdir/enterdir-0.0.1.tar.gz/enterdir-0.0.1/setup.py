import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='enterdir',
    version='0.0.1',
    author='Eduard Konanau',
    author_email='aduard.kononov@gmail.com',
    description='Simple context manager for entering and exiting a directory',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/pip_projects/enterdir',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)
