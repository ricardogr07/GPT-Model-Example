from setuptools import setup, find_packages

setup(
    name='RemoTasks-Code-Generator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',  # for accessing the OpenAI API
        'unittest',  # (optional) for running unit tests
    ],
)
