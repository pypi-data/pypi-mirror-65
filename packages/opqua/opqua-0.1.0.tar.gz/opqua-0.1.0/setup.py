from setuptools import setup

setup(
    name='opqua',
    version='0.1.0',
    description='A example Python package',
    url='https://github.com/pablocarderam/opqua',
    author='Pablo Cardenas',
    author_email='pablocarderam@gmail.com',
    license='MIT',
    packages=['opqua'],
    install_requires=['joblib',
                      'numpy',
                      'pandas',
                      'matplotlib',
                      'seaborn',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
