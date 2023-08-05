from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='pyblockpaysio',
    version='1.0.1',
    description='This library let integrate your application to our platform then use all service of cripto currencies that us have for you',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author = 'Carlos Torres - Labsatoshi',
    author_email = 'carlos.torres@labsatoshi.com',
    url = 'https://gt.globalcoin.co/ctorres/pyblockpays',
    download_url = 'https://gt.globalcoin.co/ctorres/pyblockpays/-/tree/1.0.0',
    keywords = ['blockpays', 'payments', 'criptos']
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)