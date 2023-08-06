from setuptools import setup


setup(
    name='skillcorner',
    version='0.5.0',
    description='SkillCorner API client',
    url='https://bitbucket.org/skillcorner/application',
    author='SkillCorner',
    author_email='contact@skillcorner.com',
    license='MIT',
    packages=['skillcorner'],
    # Lower versions of module could probably work, not tested though
    install_requires=[
        'python-dateutil>=2.7.3',
        'requests>=2.18',
        'websocket-client>=0.47.0'
    ]
)
