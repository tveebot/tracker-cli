from setuptools import setup, find_packages

setup(
    name='tveebot-tracker-cli',
    version='0.2',
    description='Client to interact with the tveebot-tracker',
    url='https://github.com/tveebot/tracker-cli',
    license='MIT',
    author='David Fialho',
    author_email='fialho.david@protonmail.com',

    packages=find_packages(),

    install_requires=['beautifultable', 'docopt', ],

    entry_points={
        'console_scripts': [
            'tveebot-tracker-cli=tveebot_tracker_cli:main',
        ],
    }
)
