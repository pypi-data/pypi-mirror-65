# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymispwarninglists', 'pymispwarninglists.data.misp-warninglists.tools']

package_data = \
{'': ['*'],
 'pymispwarninglists': ['data/misp-warninglists/*',
                        'data/misp-warninglists/lists/akamai/*',
                        'data/misp-warninglists/lists/alexa/*',
                        'data/misp-warninglists/lists/amazon-aws/*',
                        'data/misp-warninglists/lists/automated-malware-analysis/*',
                        'data/misp-warninglists/lists/bank-website/*',
                        'data/misp-warninglists/lists/cisco_top1000/*',
                        'data/misp-warninglists/lists/cloudflare/*',
                        'data/misp-warninglists/lists/common-contact-emails/*',
                        'data/misp-warninglists/lists/common-ioc-false-positive/*',
                        'data/misp-warninglists/lists/covid-19-cyber-threat-coalition-whitelist/*',
                        'data/misp-warninglists/lists/covid-19-krassi-whitelist/*',
                        'data/misp-warninglists/lists/covid/*',
                        'data/misp-warninglists/lists/crl-ip-hostname/*',
                        'data/misp-warninglists/lists/dax30/*',
                        'data/misp-warninglists/lists/disposable-email/*',
                        'data/misp-warninglists/lists/eicar.com/*',
                        'data/misp-warninglists/lists/empty-hashes/*',
                        'data/misp-warninglists/lists/google-gmail-sending-ips/*',
                        'data/misp-warninglists/lists/google/*',
                        'data/misp-warninglists/lists/googlebot/*',
                        'data/misp-warninglists/lists/ipv6-linklocal/*',
                        'data/misp-warninglists/lists/majestic_million/*',
                        'data/misp-warninglists/lists/microsoft-attack-simulator/*',
                        'data/misp-warninglists/lists/microsoft-azure/*',
                        'data/misp-warninglists/lists/microsoft-office365-cn/*',
                        'data/misp-warninglists/lists/microsoft-office365-ip/*',
                        'data/misp-warninglists/lists/microsoft-office365/*',
                        'data/misp-warninglists/lists/microsoft-win10-connection-endpoints/*',
                        'data/misp-warninglists/lists/microsoft/*',
                        'data/misp-warninglists/lists/moz-top500/*',
                        'data/misp-warninglists/lists/mozilla-CA/*',
                        'data/misp-warninglists/lists/mozilla-IntermediateCA/*',
                        'data/misp-warninglists/lists/multicast/*',
                        'data/misp-warninglists/lists/ovh-cluster/*',
                        'data/misp-warninglists/lists/public-dns-hostname/*',
                        'data/misp-warninglists/lists/public-dns-v4/*',
                        'data/misp-warninglists/lists/public-dns-v6/*',
                        'data/misp-warninglists/lists/rfc1918/*',
                        'data/misp-warninglists/lists/rfc3849/*',
                        'data/misp-warninglists/lists/rfc5735/*',
                        'data/misp-warninglists/lists/rfc6598/*',
                        'data/misp-warninglists/lists/rfc6761/*',
                        'data/misp-warninglists/lists/second-level-tlds/*',
                        'data/misp-warninglists/lists/security-provider-blogpost/*',
                        'data/misp-warninglists/lists/sinkholes/*',
                        'data/misp-warninglists/lists/tlds/*',
                        'data/misp-warninglists/lists/tranco/*',
                        'data/misp-warninglists/lists/university_domains/*',
                        'data/misp-warninglists/lists/url-shortener/*',
                        'data/misp-warninglists/lists/vpn-ipv4/*',
                        'data/misp-warninglists/lists/vpn-ipv6/*',
                        'data/misp-warninglists/lists/whats-my-ip/*',
                        'data/misp-warninglists/lists/wikimedia/*']}

install_requires = \
['coveralls>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'pymispwarninglists',
    'version': '1.0',
    'description': 'Python API for the MISP warning lists.',
    'long_description': '# PyMISPWarningLists\n\n[![Build Status](https://travis-ci.org/MISP/PyMISPWarningLists.svg?branch=master)](https://travis-ci.org/MISP/PyMISPWarningLists)\n[![codecov.io](https://codecov.io/github/MISP/PyMISPWarningLists/coverage.svg?branch=master)](https://codecov.io/github/MISP/PyMISPWarningLists?branch=master)\n\nPythonic way to work with the warning lists defined there: https://github.com/MISP/misp-warninglists\n\n# Installation\n\n`pip install pymispwarninglists`\n\n# Usage\n\nWarning lists are represented as immutable Python dictionaries.\n\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
