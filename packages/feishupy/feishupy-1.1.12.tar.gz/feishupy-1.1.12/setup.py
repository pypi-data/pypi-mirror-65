from setuptools import setup, find_packages

setup(
    name="feishupy",
    version='1.1.12',
    packages=find_packages(exclude=('tests', 'tests.*')),
    description="A package for FeiShu, Implement API.",
    author="WUWUTech",
    author_email='wuwu@wuwu.tech',
    url="https://github.com/WUWUTech/feishupy",
    keywords=['feishupy', 'feishu', 'SDK'],
    classifiers=[
        'Environment :: Console',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        "enum34>=1.1.4; python_version < '3.4'",
        'tls-sig-api-v2>=1.1',
        'requests>=2.4.3'
    ]
)
