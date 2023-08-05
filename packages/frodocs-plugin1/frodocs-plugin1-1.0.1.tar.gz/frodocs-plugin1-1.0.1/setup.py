from setuptools import setup, find_packages


setup(
    name='frodocs-plugin1',
    version='1.0.1',
    description='Test a plugin',
    long_description='None',
    keywords='frodocs python markdown wiki',
    url='https://frodo.ga',
    author='Ham',
    author_email='lwonderlich@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'frodocs>=1'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
    entry_points={
        'frodocs.plugins': [
            'plugin1 = frodocs_plugin1.plugin:FrodocsPlugin1'
        ]
    }
)
