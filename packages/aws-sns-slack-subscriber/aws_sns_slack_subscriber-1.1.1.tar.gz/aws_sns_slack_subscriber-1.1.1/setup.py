from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='aws_sns_slack_subscriber',
    version='1.1.1',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=('AWS package which creates a Slack subscriber to a SNS Topic.'),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'aws_cdk.core==1.27.0',
        'aws_cdk.aws_lambda==1.27.0',
        'aws_cdk.aws_sns==1.27.0',
        'aws_cdk.aws_sns_subscriptions==1.27.0',
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@gmail.com (laimonas@idenfy.com)',
    keywords='AWS SNS Topic Slack Lambda',
    url='https://github.com/idenfy/AwsSnsSlackSubscriber.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
