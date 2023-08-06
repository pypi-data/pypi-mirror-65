from setuptools import setup, find_packages

setup(
    name="flylog_robot",
    version='0.0.5',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['requests', 'redis'],
    scripts=['flylog/bin/run_flylog.py'],
    url="https://github.com/sbfksmq/flylog",
    license="BSD",
    author="lijifeng",
    author_email="sbfksmq@outlook.com",
    description="make log fly to mail or other or robot",
)
