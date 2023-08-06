from setuptools import setup

setup(
    name='audio_processing',
    version='0.0.1',
    description='Package providing basic functionality for handling Waveform objects in a audio processing pipeline',
    py_modules=["datatypes"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        
    ],
    setup_requires=[
        "numpy >= 1.18.1",
        "librosa >= 0.7.2",
    ]
)