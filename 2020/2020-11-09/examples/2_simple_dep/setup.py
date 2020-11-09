from setuptools import setup


setup(
    name="mysuperduperproject",
    description="My super duper Project.",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
    ],
    license='MIT License',
    package_dir={
        '': 'src'
    },
    packages=[
      'msdp',
    ],
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@gmail.com',
    install_requires=[
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "msdp-hello=msdp.hello:sys_main",
        ]
    }
)
