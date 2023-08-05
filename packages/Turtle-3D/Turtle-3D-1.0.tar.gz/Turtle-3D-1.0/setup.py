from setuptools import setup, find_packages


setup(
    name='Turtle-3D',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/Heono',
    license='MIT',
    author='Heono',
    author_email='chooheonoh@gmail.com',
    description='Python Turtle Graphics in 3D',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pyzmq==19.0.0'
    ]
)
