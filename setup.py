from setuptools import setup, find_packages

setup(
    name='guess-the-word.python',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',  # Your Flask app's dependencies
        'Flask-Mail',
        'Jinja2', # Move Pillow to core lib
        'python-dotenv',
        'gunicorn',
        'werkzeug',
        'boto3',
        'botocore',
        # Testing
        'pytest',
        'pytest-cov',
        'pytest-flask',
        'pytest-mock',
        # Code Quality
        'black',
        'flake8',
        'mypy',
        'isort',
        # Development Tools
        'pre-commit',
        'python-dotenv',
    ],
)