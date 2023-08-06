from setuptools import setup

setup(
    name='ehr-functions',
    packages=['ehr_functions'],
    version='0.1.0',
    license='MIT',
    description='A library for EHR related functions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Filip Dabek',
    url='https://github.com/fdabek1/ehr-functions',
    download_url='https://github.com/fdabek1/ehr-functions/archive/v0.1.0.tar.gz',
    keywords=['ehr', 'functions', 'library'],
    install_requires=[
        'keras',
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
