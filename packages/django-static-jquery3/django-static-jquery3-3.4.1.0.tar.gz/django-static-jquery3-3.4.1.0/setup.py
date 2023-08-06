import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()
requires = [x.strip() for x in requires if x.strip()]

setup(
    name="django-static-jquery3",
    version="3.4.1.0",
    description="Django application contain jquery3 static files.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="appstore@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['django-static-jquery3'],
    packages=find_packages("."),
    requires=requires,
    install_requires=requires,
    zip_safe=False,
    include_package_data=True,
)
