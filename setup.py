import pathlib
import setuptools

PACKAGE_NAME = 'coollect'
REQS_FILE = pathlib.Path(__file__).parent / 'requirements.txt'
REQS = []
if REQS_FILE.is_file():
    with open('requirements.txt', 'r') as reader:
        reqs = reader.read().splitlines()

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    url='http://github.com/DanielSolomon/coollect',
    author='Daniel Solomon',
    author_email='DanielSolomon94.ds@gmail.com',
    license='MIT',
    packages=[PACKAGE_NAME],
    zip_safe=False,
    install_requires=REQS,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)