from setuptools import setup

setup(
    name='bead_it',
    version='0.01',
    packages=['bead_it'],
    url='https://github.com/DevinHA/bead_it.git',
    license='',
    author='huangzijing',
    description='A simple code to count number of pixels in an image',
    entry_points={
          'console_scripts': [
              'bead_it = bead_it.count:main'
          ]
    },
    install_requires=[
        'webcolors',
        'Pillow>=5.3.0'
    ],
    setup_requires=[
        'webcolors',
        'Pillow>=5.3.0'
    ]
)
