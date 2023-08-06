from distutils.core import setup

setup(
    name='imagescraperwithbrowser',
    packages=['imagescraperwithbrowser'],
    version='0.1',
    license='gpl-3.0',
    description='Scrap images from websites with browser',
    author='Egehan Dulger',
    url='https://github.com/egehandulger/image-scrapper-with-browser',
    download_url='https://github.com/egehandulger/image-scraper-with-browser/archive/v0.1.tar.gz',
    keywords=['image', 'search', 'scrap', 'save', 'download'],
    install_requires=['selenium', 'tqdm', 'logdecorator'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
