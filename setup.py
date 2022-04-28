from setuptools import setup, find_packages

REQUIREMENTS_FILE_PATH = 'requirements.txt'


def load_requirements():
    with open(REQUIREMENTS_FILE_PATH) as file:
        return file.read().splitlines()


setup(
    name='moonlan',
    version='0.1.0',
    description='Serve the LAN info',
    author='Elai Corem',
    packages=find_packages(include=['moonlan', 'moonlan.*']),
    install_requires=load_requirements(),
    entry_points={
        'console_scripts': ['moonlan=moonlan.__main__:main']
    },
)
