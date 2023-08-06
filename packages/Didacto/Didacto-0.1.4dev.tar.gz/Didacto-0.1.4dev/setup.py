from distutils.core import setup

setup(
    name='Didacto',
    version='0.1.4dev',
    author='Marco de Freitas',
    author_email='marco@silage.ch',
    packages=['didacto'],
    url='https://gitlab.inubo.ch/glag/didacto',
    license='LICENSE.txt',
    description='Indexing pdf corpora keywords fields',
    long_description=open('README.txt').read(),
    long_description_content_type='text/x-rst',
    install_requires=[
        "PyPDF2 >= 1.26.0",
    ],
)
