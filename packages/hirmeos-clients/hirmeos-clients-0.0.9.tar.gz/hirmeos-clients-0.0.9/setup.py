from setuptools import setup


with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='hirmeos-clients',
    version='0.0.9',
    author='Rowan Hatheryley',
    author_email='rowan.hatherley@ubiquitypress.com',
    description='Python API clients for the HIRMEOS project.',
    install_requires=[
        'requests>=2.22.0',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/rowan08/hirmeos-clients',  # TODO: Change when live
    packages=['hirmeos_clients'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7'
)
