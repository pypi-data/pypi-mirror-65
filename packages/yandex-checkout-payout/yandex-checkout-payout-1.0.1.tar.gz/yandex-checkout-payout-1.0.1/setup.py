#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from setuptools import setup, find_packages  # type: ignore

with open("README.en.md") as readme_file:
    readme = readme_file.read()

with open('src/yandex_checkout_payout/__init__.py', encoding='utf8') as fp:
    version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

setup(
    author="Yandex Money",
    author_email="cms@yamoney.ru",
    version=version,
    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="",
    entry_points={"console_scripts": ["ym-payout=yandex_checkout_payout.cli:main", ], },
    install_requires=['urllib3', 'requests', 'lxml', 'python-dateutil', 'pyOpenSSL'],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_data={"yandex_checkout_payout": ["py.typed"]},
    include_package_data=True,
    keywords="yandex, checkout, payout, sdk, python",
    name="yandex-checkout-payout",
    package_dir={"": "src"},
    packages=find_packages('src'),
    setup_requires=[],
    url="https://github.com/yandex-money/yandex-checkout-payout-sdk-python",
    zip_safe=False,
)
