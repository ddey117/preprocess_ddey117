import setuptools

with open('README.md', 'r') as fn:
    long_description = fn.read()

setuptools.setup(
    name = 'preprocess_ddey117',  #must be unique
    version = '0.0.1',
    author = 'Dylan Dey',
    author_email = 'ddey2985@gmail.com',
    description = 'Text data preprocessing package',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = setuptools.find_packages(),
    classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent']
    python_requires = '>=3.5'
    )
    
