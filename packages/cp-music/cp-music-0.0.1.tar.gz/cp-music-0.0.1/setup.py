from setuptools import setup, find_packages


with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='cp-music',
    version='0.0.1',
    url='https://github.com/CorbinMoon/cp-music',
    author='Corbin Moon',
    author_email='clangmoon@gmail.com',
    description="A small library for constraint programming with musicxml in python using ortools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Source': 'https://github.com/CorbinMoon/cp-music'
    },
    packages=find_packages(),
    install_requires=['ortools'],
    python_requires='>=3.6, <=3.7',
    package_data={
        'examples': ['example1.musicxml']
    }
)
