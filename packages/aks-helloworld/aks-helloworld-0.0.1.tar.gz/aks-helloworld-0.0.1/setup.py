from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
        name='aks-helloworld',
        version='0.0.1',
        description='My hello world',
        py_modules=['helloworld'],
        package_dir={'': 'src'},
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='http://www.google.com',
        author='Anand Saha',
        author_email='foo@bar.com',
        install_requires = [
            'blessings ~= 1.7',
        ],
        extras_require = {
            'dev': [
                'pytest>=3.7',
            ],
        },
)
