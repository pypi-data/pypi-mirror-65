from setuptools import setup

setup(
    name = 'astylo',
    version = '0.2',
    author = 'D. HU',
    author_email = 'dangning.hu@cea.fr',
    description = 'Python tool kit based on astropy, etc.',
    license = 'BSD',
    keywords = 'astronomy astrophysics',
    url = 'https://github.com/kxxdhdn/astylo',

    python_requires='>=3.6',
    install_requires = [
        'numpy', 'scipy', 'matplotlib', 
        'astropy', 'reproject', 'h5py', 'tqdm', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    
    ## Plugins
    entry_points={
        # Installation test with command line
        'console_scripts': [
            'astyloading = astylo:iTest',
        ],
    },

    ## Packages
    packages = ['astylo'],

    ## Package data
    package_data = {
        # include *.txt files in astylo/data
        'astylo': ['dat/*.txt'],
    },
)
