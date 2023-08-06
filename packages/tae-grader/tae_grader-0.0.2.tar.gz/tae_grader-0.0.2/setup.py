from setuptools import setup

setup (
    name = 'tae_grader',
    version = '0.0.2',
    description = 'TAE Grader',
    install_required= [
        'pygments',
        'jinja2'
    ],
    packages = ['tae_grader'],
)
