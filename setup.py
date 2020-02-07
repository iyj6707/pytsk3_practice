from setuptools import setup, find_packages


setup(
    name='lib',
    version='1.0.0',
    author='Im yeonjae',
    author_email='iyj6707@naver.com',
    url='https://github.com/iyj6707',
    description='This is practice for coding test',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "coding_test = lib.main:main"
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'pytsk3'
    ],
)
