from distutils.core import setup

setup(
    name='slata-parser',
    packages=['slata_parser'],
    version='0.2.2',
    license='MIT',
    description='Slata shop parser.',
    author='retxxxirt',
    author_email='retxxirt@gmail.com',
    url='https://github.com/retxxxirt/slata-parser',
    keywords=['slata', 'slata parser', 'slata api', 'slata crawler'],
    install_requires=['requests==2.23.0', 'beautifulsoup4==4.8.2']
)
