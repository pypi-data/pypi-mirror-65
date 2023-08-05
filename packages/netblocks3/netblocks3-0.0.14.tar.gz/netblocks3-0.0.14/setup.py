# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netblocks3']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'netblocks3',
    'version': '0.0.14',
    'description': 'Get the Cloud Provider netblocks (Python3 version)',
    'long_description': '# Netblocks\n\n**This is not an official Google product.**\n\nThis module retrieves the DNS entries recursively as per the below links\n\n    The GCE ranges\n        https://cloud.google.com/compute/docs/faq#where_can_i_find_product_name_short_ip_ranges\n    The Google Services ranges\n        https://support.google.com/a/answer/60764\n    The AWS ranges\n        https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html\n\nInstall the package with `pip install netblocks` or `pip install git+https://github.com/hm-distro/netblocks/`\n\nThe `fetch()` method has the default parameter value of `initial_dns_list=[GOOGLE_INITIAL_CLOUD_NETBLOCK_DNS, GOOGLE_INITIAL_SPF_NETBLOCK_DNS]`\n\nwhere \n\n    #The GCE ranges\n    GOOGLE_INITIAL_CLOUD_NETBLOCK_DNS = "_cloud-netblocks.googleusercontent.com"\n\n    #The Google Services ranges\n    GOOGLE_INITIAL_SPF_NETBLOCK_DNS= "_spf.google.com"\n\n    #The AWS ranges\n    AWS_IP_RANGES="https://ip-ranges.amazonaws.com/ip-ranges.json"\n\nSee [here](https://github.com/hm-distro/netblocks) on how to use this module in Google App Engine  \n### API Usage\n\n    import netblocks\n    cidr_blocks = set()\n    api = netblocks.NetBlocks()\n    try:\n        # returns both GOOGLE_INITIAL_CLOUD_NETBLOCK_DNS and GOOGLE_INITIAL_SPF_NETBLOCK_DNS\n        cidr_blocks = api.fetch()\n        \n        # To get only the SPF list use the below:\n        #  cidr_blocks = api.fetch([netblocks.GOOGLE_INITIAL_SPF_NETBLOCK_DNS])\n \n        \n        # To get only the GCE list use the below:\n        #  cidr_blocks = api.fetch([netblocks.GOOGLE_INITIAL_CLOUD_NETBLOCK_DNS]) \n        \n        # To get only the AWS list use the below:\n        #  cidr_blocks = api.fetch([netblocks.AWS_IP_RANGES]) \n        \n        """\n        The cidr_blocks set contains strings like the below\n        ip4:146.148.2.0/23\n        ...\n        ip6:2600:1900::/35\n        """\n        \n    except netblocks.NetBlockRetrievalException as err:\n        #exception handling\n        pass\n\n## Language\n- [Python](https://www.python.org/)\n\n## Dependencies\nrequests\n\n## License\nApache 2.0; see [LICENSE](https://github.com/hm-distro/netblocks/blob/master/netblocks/LICENSE) for details.',
    'author': 'hm-distro',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
