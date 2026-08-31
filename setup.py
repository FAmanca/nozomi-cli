from setuptools import setup

setup(
    name='anisub',
    version='0.1.0',
    py_modules=['main', 'api', 'config', 'history', 'user_config'],
    install_requires=[
        'InquirerPy',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'anisub=main:start',
        ],
    },
    python_requires='>=3.8',
    author='FAmanca',
    description='CLI untuk streaming anime subtitle Indonesia ala ani-cli',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)
