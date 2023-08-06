from setuptools import setup

setup(
    name='hive_tagbot',
    version='0.1.0',
    packages=["tagbot",],
    url='http://github.com/emre/tagbot',
    license='MIT',
    author='emre yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Random upvote bot on specific tags on HIVE network',
    entry_points={
        'console_scripts': [
            'tagbot = tagbot.bot:main',
        ],
    },
    install_requires=["hivepy", "nltk", "requests"]
)
