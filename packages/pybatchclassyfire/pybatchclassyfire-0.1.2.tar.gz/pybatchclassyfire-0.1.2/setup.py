from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()
    

setup(
    name='pybatchclassyfire',

    version='0.1.2',

    description='A python client for the ClassyFire API',

    url='https://gitlab.unige.ch/Pierre-Marie.Allard/pybatchclassyfire.git',

    author='Pierre-Marie Allard',
    author_email='pierre-marie.allard@unige.ch',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Chemistry',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='Cheminformatics ClassyFire ontology',

    packages=['pybatchclassyfire'],

    install_requires=['requests'],

    extras_require={
        'sdf_query': ['rdkit'],
    },
)
