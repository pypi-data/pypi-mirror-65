import setuptools

setuptools.setup(
    name='flow_vis',
    packages=['flow_vis'],
    version='0.1',
    license='MIT',
    author='Tom Runia',
    author_email='firstname.lastname@gmail.com',
    description='Easy optical flow visualisation in Python.',
    long_description='Python port of the optical flow visualization: https://people.csail.mit.edu/celiu/OpticalFlow/',
    url='https://github.com/tomrunia/OpticalFlow_Visualization',
    download_url='https://github.com/tomrunia/OpticalFlow_Visualization/archive/0.1.tar.gz',
    keywords=['optical flow', 'visualization', 'motion'],
    install_requires=['numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)