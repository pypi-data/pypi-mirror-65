import pathlib
import pipfile
import setuptools


ROOT = pathlib.Path(__file__).parent
PIP_FILE = ROOT / 'Pipfile'
PACKAGE_NAME = 'ctests'

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    url=f'http://github.com/DanielSolomon/{PACKAGE_NAME}',
    author='Daniel Solomon',
    author_email='DanielSolomon94.ds@gmail.com',
    license='MIT',
    packages=[PACKAGE_NAME],
    zip_safe=False,
    install_requires=list(pipfile.load(str(PIP_FILE)).data['default'].keys()),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
