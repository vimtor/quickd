from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


setup(
    name='quickd',
    version='0.1.1',
    license='MIT',
    author='Victor Navarro',
    author_email='victor@vimtor.io',
    description='Decorator type based dependency injection',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vimtor/quickd',
    project_urls={
        "Bug Tracker": "https://github.com/vimtor/quickd/issues",
    },
    install_requires=[],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    keywords=['dependency injection', 'unif of work', 'decorators', 'typings'],
    extras_require={
        'tests': ['pytest'],
        'build': ['twine', 'wheel']
    },
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
