from setuptools import setup
 
setup(
    name='sklearnkernels',
    packages=['sklearnkernels'], 
    version='0.1.0',
    license='GPL', 
    description='A random test lib',
    author='Mora Hector',
    author_email='hector.mora@gmail.com',
    url='https://github.com/magohector/sklearnkernels/tree/master/sklearnkernels', 
    download_url='https://github.com/magohector/sklearnkernels/archive/V0.1.0.tar.gz', 
    keywords='ANN, SVM, Kernels', 
    classifiers=['Programming Language :: Python',  
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7'],
    
    install_requires=[
        'numpy>=1.9.3',
        'scipy>=0.16.0',        
        'scikit-learn>=0.18.0',
    ],
)
