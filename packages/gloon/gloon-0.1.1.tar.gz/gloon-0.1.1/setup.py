from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='gloon',
    version='0.1.1',
    description='Download file from your file cabinet and open Visual Code diff tool',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Octavio Quiroz',
    author_email='octavioquiroz30@gmail.com',
    keywords=['Netsuite'],
    url='',
    download_url='',
    include_package_data=True
)
install_requires = [
    'PyInquirer>=1.0.3',
    'halo>=0.0.29',
    'zeep>=3.4.0'
]
if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)