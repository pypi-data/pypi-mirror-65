from setuptools import setup


def readme():
    """Read README file"""
    with open('README.md') as infile:
        return infile.read()


setup(
    name='ratelimit-stubs',
    version='2.2.1',
    description='Stub for ratelimit',
    long_description=readme().strip(),
    author='Byeonghoon Yoo',
    author_email='bh322yoo@gmail.com',
    url='https://github.com/isac322/ratelimit-stubs',
    license='MIT',
    packages=['ratelimit-stubs'],
    install_requires=[],
    keywords=[
        'ratelimit',
        'api',
        'decorator',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
    package_data={
        '': ['*.pyi'],
    },
    zip_safe=False
)
