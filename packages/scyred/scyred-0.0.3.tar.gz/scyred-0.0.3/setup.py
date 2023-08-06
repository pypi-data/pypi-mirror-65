from setuptools import setup

setup(
    name='scyred',
    version='0.0.3',
    url='https://github.com/caiocarneloz/scyred',
    license='MIT License',
    author='Caio Carneloz',
    author_email='caiocarneloz@gmail.com',
    keywords='optimizer',
    description=u'Library that joins scikit-learn with inspyred to create an easy-to-use parameter tuning',
    packages=['scyred'],
    install_requires=['inspyred', 'sklearn'],
)