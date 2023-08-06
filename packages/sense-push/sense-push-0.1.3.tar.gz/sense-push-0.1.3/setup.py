import os
from setuptools import setup

requirements = [
    "sense_core>=0.2.61",
    "django"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sense-push',
    version='0.1.3',
    packages=[
        "sense_push",
        "sense_push.core",
        "sense_push.common",
        "sense_push.util",
    ],
    license='BSD License',  # example license
    description='sense push',
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url='',
    author='kafka0102',
    author_email='yujianjia@sensedeal.ai',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
