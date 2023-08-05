from setuptools import setup


with open('README.rst') as f:
    long_description = f.read()

setup(
    name="behvpn",
    version="2.3.2",
    license='MIT',
    description="A fast tunnel proxy that help you get through firewalls",
    author='3epter',
    author_email='sepehr.r201400@gmail.com',
    url='https://github.com/cep-ter/behvpn',
    packages=['behvpn', 'behvpn.crypto'],
    package_data={
        'behvpn': ['README.rst', 'LICENSE']
    },
    install_requires=[],
    entry_points="""
    [console_scripts]
    behvpn = behvpn.local:main
    behserver = behvpn.server:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Proxy Servers',
    ],
    long_description=long_description,
)
