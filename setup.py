import setuptools

setuptools.setup(
    name='roa-collector',
    version='0.1.1',
    description='RPKI ROA data file collector',
    author='Mingwei Zhang, Cecilia Testart',
    author_email='mingwei@caida.org',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        # available on pip
        "beautifulsoup4",
        "argparse",
        "requests",
        "backports-datetime-fromisoformat",  # for python version before 3.7
    ],
    entry_points={'console_scripts': [
        "roa-collector = collector.collector:main",
    ]}
)
