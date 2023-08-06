from setuptools import setup, find_packages
import io


packages = [
    'requests>=2.18.4',
    'bert-serving-client==1.9.6',
    'pyzmq>=17.1.2',
    'numpy',
    'scipy',
    'scikit-learn',
    'tqdm'
]

setup(
    name='nlutools',
    version=open("nlutools/config/version.txt").read().strip(),
    description='nlu service tools',
    long_description=io.open('README.md', 'r', -1, 'utf-8').read(),
    long_description_content_type="text/markdown",
    url='https://www.ifchange.com',
    author='ai3',
    author_email='ai3@ifchange.com',
    license='Apache License 2.0',
    install_requires=packages,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'nlu=nlutools.cli:main'
        ]
    }
)
