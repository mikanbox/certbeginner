from setuptools import setup


setup(
        name='certbeginner',
        version='1.0.0',
        install_requires=['argparse'],
        entry_points={
            "console_scripts": ['crtbg = src.app:main']
        }
)