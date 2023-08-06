from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

setup(
    name='markdown_vimwiki',
    version='0.1.2',
    description='Markdown extension for vimwiki todos and tags',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Madison Scott-Clary',
    author_email='makyo@drab-makyo.com',
    packages=['markdown_vimwiki'],
    install_requires=['markdown'],
    url='https://github.com/makyo/markdown-vimwiki',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing',
        'Programming Language :: Python :: 3',
    ])
