from setuptools import setup

setup(
    name='blacksock',
    version='0.1.0',
    description='An OpenCV app to turn a webcom into a virtual midi controller.',
    url='https://github.com/arkocal/black-sock',
    author='Ali Rasim Kocal',
    author_email='arkocal@posteo.net',
    license='GPLv3',
    packages=['blacksock'],
    install_requires=['python-rtmidi',
                      'opencv-python',
                      'numpy'
                      ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3'
    ],
)
