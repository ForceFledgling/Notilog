from setuptools import setup, find_packages

setup(
    name='notilog',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # укажите зависимости здесь
    ],
    entry_points={
        'console_scripts': [
            'notilog-server=notilog.server.api:main',
            'notilog-agent=notilog.client.agent:main',
        ],
    },
)
