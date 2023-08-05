# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='patul',
    version=0.1001,
    description=(
        'A tiny spider based on asyncio and requests.'
    ),
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='financial',
    author_email='1012593988@qq.com',
    maintainer='financial',
    maintainer_email='1012593988@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/financialfly/patul',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
            'requests>=2.14.0',
            'parsel>=1.5.1'
        ]
)