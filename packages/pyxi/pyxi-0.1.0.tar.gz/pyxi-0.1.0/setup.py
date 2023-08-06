import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
        name='pyxi',
        version='0.1.0',
        author='Rob Wagner',
        author_email='rob.wagner@outlook.com',
        description='A small library for interacting with `.pyxel` files from PyxelEdit.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/robertwayne/pyxi',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3.8',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Typing :: Typed',
            'Intended Audience :: Developers',
            'Development Status :: 3 - Alpha',
        ],
        python_requires='>=3.8',
)
