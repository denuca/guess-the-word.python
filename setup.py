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
        'pytest',
        'werkzeug',
        'boto3',
        'botocore'
    ],
)