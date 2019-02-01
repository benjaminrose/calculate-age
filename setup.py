from setuptools import setup, find_packages

#TODO Update this to pull from __init__.py.
setup(
    name='calculate_age',
    version='0.1',
    description='A way to calculate the age from a given SFH',
    # long_description='',
    author='Benjamin Rose',
    aurhor_email='benjamin.rose@me.com',
    url='',
    license='MIT',
    keywords='astronomy astrophysics age star',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Programming Language :: Python :: 3 :: Only',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering :: Astronomy',
                 'License :: OSI Approved :: MIT License'],
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=["calculate_age"],  # may skip looking at calculate_age/__init__.py
    install_requires=[
        'numpy',
        'scipy',
        'astropy'],
)
