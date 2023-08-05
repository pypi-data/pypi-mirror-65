from setuptools import setup, find_packages
import sys
import os
import time


def publish():
    """Publish to PyPi"""
    print('publishing...')
    os.system("rm -rf dist wonderbitscloud.egg-info build")
    os.system("python3 setup.py sdist build")
    os.system("twine upload dist/*")
    os.system("rm -rf dist wonderbitscloud.egg-info build")


def _auto_version(version=''):
    import time
    import json
    # read version from file
    with open('cloud/__version__.py', 'rb') as f:
        ver = json.loads(f.readline().decode('utf-8'))

    ver['published time'] = time.strftime(
        '%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
    if version:
        ver['version'] = list(map(int, version.split('.')))
    else:
        ver['version'][2] += 1

    # storage version to file
    with open('cloud/__version__.py', 'wb') as f:
        f.write(json.dumps(ver).encode('utf-8'))

    return '.'.join(map(str, ver['version']))


if sys.argv[-1] == "-p":
    publish()
    sys.exit()

setup(
    name='wonderbitscloud',
    version=_auto_version(),
    # version=_auto_version('1.2.2'),
    description=('wonderbitscloud allows you to use variables remotely.'),
    long_description=open('README.rst').read(),
    author='mfe',
    author_email='account@mfeducation.cn',
    maintainer='mfe',
    maintainer_email='account@mfeducation.cn',
    license='MIT License',
    install_requires=[],
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    # entry_points={
    #     'console_scripts': [
    #         'cloudvar=cloudvar.cli:cli',
    #     ],
    # },
)

# python3 setup.py -p
