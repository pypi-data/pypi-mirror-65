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
    'version': '0.0.13rc2',
    'description': 'Get the Cloud Provider netblocks (Python3 version)',
    'long_description': '# Netblocks\n\n**This is not an official Google product.**\n\nThis is a [Google App Engine](https://cloud.google.com/appengine/) app that regularly checks the DNS entries using the [netblocks](https://github.com/hm-distro/netblocks/blob/master/netblocks/README.md) module.\nThis App engine code updates the GCS bucket, when there is a change in the CIDR blocks for GCE.\n\nThe netblocks api module itself can be used outside App Engine.\nInstall the package with `pip install netblocks` or `pip install git+https://github.com/hm-distro/netblocks/`\n    \nDownstream systems can hook into the Object notification on the [GCS bucket](https://cloud.google.com/storage/docs/object-change-notification) and accordingly\ndo something with the file, with the updated CIDR ranges.\nThe schedule of this refresh can be managed in the cron.yaml and the bucket and file where the CIDR ranges should be written to can be changed in the config.py\n\nPotential listeners could be [Cloud Functions](https://cloud.google.com/functions/).\n\n\n### API Usage\n\n    import netblocks\n    cidr_blocks = set()\n    netblocks_api = netblocks.NetBlocks()\n    try:\n        cidr_blocks = netblocks_api.fetch()\n        \n        """\n        The cidr_blocks set contains strings like the below\n        ip4:146.148.2.0/23\n        ...\n        ip6:2600:1900::/35\n        """\n        \n    except netblocks.NetBlockRetrievalException as err:\n        #exception handling\n        pass\n\n### The GAE App\n*  UpdateGCSBucket </br>\n\n This class creates a file in the GCS bucket as specified in config.py.<br/>\n The files contains entries such as the below: <br/>\n ip4:146.148.2.0/23<br/>\n ...<br/>\n ip6:2600:1900::/35<br/>\n Make sure to create a bucket prior to deploying the app<br/>\n This bucket-name should be changed in the config.py under GCS_BUCKET\n \n Deploy using \n \n `gcloud app  deploy app.yaml`\n \n `gcloud app  deploy cron.yaml`\n \n  \n \n## Products\n- [Google App Engine](https://cloud.google.com/appengine/)\n\n## Language\n- [Python](https://www.python.org/)\n\n## Dependencies\nRun these steps before deploying the app <br/>\nmkdir lib <br/>\npip install -t ./lib/ google-api-python-client <br/>\npip install -t ./lib/ GoogleAppEngineCloudStorageClient <br/> \npip install -t ./lib/ requests <br/>\npip install -t ./lib/ oauth2client <br/> \npip install -t ./lib/ requests-toolbelt <br/>\n\n## License\nApache 2.0; see [LICENSE](LICENSE) for details.\n',
    'author': 'tomasfse',
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
